"""
轻量级医学科普文章生成服务

职责：
1. 基于表单参数规划文章大纲
2. 逐章节调用 LLM 生成 markdown 内容
3. 维护文章元数据、进度和 JSONL 执行日志
4. 提供基于全文上下文的聊天能力
"""

import json
import os
import re
import threading
import time
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from ..config import Config
from ..models.task import TaskManager, TaskStatus
from ..utils.llm_client import LLMClient
from ..utils.logger import get_logger

logger = get_logger('mirofish.article_agent')


class ArticleLogger:
    """文章生成结构化日志记录器（JSONL）"""

    def __init__(self, article_id: str):
        self.article_id = article_id
        self.log_file_path = ArticleManager.get_agent_log_path(article_id)
        self.start_time = datetime.now()
        os.makedirs(os.path.dirname(self.log_file_path), exist_ok=True)

    def _elapsed_seconds(self) -> float:
        return round((datetime.now() - self.start_time).total_seconds(), 2)

    def log(
        self,
        action: str,
        stage: str,
        details: Dict[str, Any],
        section_title: Optional[str] = None,
        section_index: Optional[int] = None
    ) -> None:
        entry = {
            "timestamp": datetime.now().isoformat(),
            "elapsed_seconds": self._elapsed_seconds(),
            "article_id": self.article_id,
            "action": action,
            "stage": stage,
            "section_title": section_title,
            "section_index": section_index,
            "details": details,
        }
        with open(self.log_file_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')


class ArticleManager:
    """文章文件管理器"""

    _write_lock = threading.Lock()

    @classmethod
    def _base_dir(cls) -> str:
        return os.path.join(Config.UPLOAD_FOLDER, 'articles')

    @classmethod
    def get_article_dir(cls, article_id: str) -> str:
        return os.path.join(cls._base_dir(), article_id)

    @classmethod
    def get_meta_path(cls, article_id: str) -> str:
        return os.path.join(cls.get_article_dir(article_id), 'meta.json')

    @classmethod
    def get_progress_path(cls, article_id: str) -> str:
        return os.path.join(cls.get_article_dir(article_id), 'progress.json')

    @classmethod
    def get_agent_log_path(cls, article_id: str) -> str:
        return os.path.join(cls.get_article_dir(article_id), 'agent_log.jsonl')

    @classmethod
    def ensure_article_folder(cls, article_id: str) -> None:
        os.makedirs(cls.get_article_dir(article_id), exist_ok=True)

    @classmethod
    def _write_json(cls, path: str, data: Dict[str, Any]) -> None:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with cls._write_lock:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

    @classmethod
    def _read_json(cls, path: str) -> Optional[Dict[str, Any]]:
        if not os.path.exists(path):
            return None
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    @classmethod
    def create_article(cls, article_id: str, task_id: str, form_data: Dict[str, Any]) -> Dict[str, Any]:
        cls.ensure_article_folder(article_id)
        now = datetime.now().isoformat()
        meta = {
            "article_id": article_id,
            "task_id": task_id,
            "status": "pending",
            "created_at": now,
            "updated_at": now,
            "form_data": form_data,
            "outline": None,
            "generated_sections": {},
            "markdown_content": "",
            "error": None,
        }
        cls._write_json(cls.get_meta_path(article_id), meta)
        cls.update_progress(article_id, status="pending", progress=0, message="任务已创建")
        return meta

    @classmethod
    def get_article(cls, article_id: str) -> Optional[Dict[str, Any]]:
        return cls._read_json(cls.get_meta_path(article_id))

    @classmethod
    def save_article(cls, article_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        data["updated_at"] = datetime.now().isoformat()
        cls._write_json(cls.get_meta_path(article_id), data)
        return data

    @classmethod
    def update_article(cls, article_id: str, **fields: Any) -> Dict[str, Any]:
        meta = cls.get_article(article_id)
        if not meta:
            raise FileNotFoundError(f"文章不存在: {article_id}")
        meta.update(fields)
        return cls.save_article(article_id, meta)

    @classmethod
    def update_progress(
        cls,
        article_id: str,
        status: str,
        progress: int,
        message: str,
        current_section: Optional[str] = None,
        completed_sections: Optional[List[str]] = None,
        error: Optional[str] = None
    ) -> Dict[str, Any]:
        payload = {
            "article_id": article_id,
            "status": status,
            "progress": max(0, min(100, progress)),
            "message": message,
            "current_section": current_section,
            "completed_sections": completed_sections or [],
            "updated_at": datetime.now().isoformat(),
            "error": error,
        }
        cls._write_json(cls.get_progress_path(article_id), payload)
        return payload

    @classmethod
    def get_progress(cls, article_id: str) -> Optional[Dict[str, Any]]:
        return cls._read_json(cls.get_progress_path(article_id))

    @classmethod
    def save_outline(cls, article_id: str, outline: Dict[str, Any]) -> Dict[str, Any]:
        meta = cls.get_article(article_id)
        if not meta:
            raise FileNotFoundError(f"文章不存在: {article_id}")
        meta["outline"] = outline
        meta["status"] = "planning"
        return cls.save_article(article_id, meta)

    @classmethod
    def save_section(cls, article_id: str, section_index: int, section_title: str, content: str) -> Dict[str, Any]:
        meta = cls.get_article(article_id)
        if not meta:
            raise FileNotFoundError(f"文章不存在: {article_id}")
        generated_sections = meta.get("generated_sections") or {}
        generated_sections[str(section_index)] = {
            "title": section_title,
            "content": content,
        }
        meta["generated_sections"] = generated_sections
        meta["status"] = "generating"
        return cls.save_article(article_id, meta)

    @classmethod
    def complete_article(cls, article_id: str, markdown_content: str) -> Dict[str, Any]:
        meta = cls.get_article(article_id)
        if not meta:
            raise FileNotFoundError(f"文章不存在: {article_id}")
        meta["status"] = "completed"
        meta["markdown_content"] = markdown_content
        meta["error"] = None
        return cls.save_article(article_id, meta)

    @classmethod
    def fail_article(cls, article_id: str, error: str) -> Dict[str, Any]:
        meta = cls.get_article(article_id)
        if not meta:
            raise FileNotFoundError(f"文章不存在: {article_id}")
        meta["status"] = "failed"
        meta["error"] = error
        return cls.save_article(article_id, meta)

    @classmethod
    def get_agent_log(cls, article_id: str, from_line: int = 0) -> Dict[str, Any]:
        path = cls.get_agent_log_path(article_id)
        if not os.path.exists(path):
            return {
                "logs": [],
                "total_lines": 0,
                "from_line": from_line,
                "has_more": False,
            }

        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        total_lines = len(lines)
        selected_lines = lines[from_line:]
        logs = [json.loads(line) for line in selected_lines]

        return {
            "logs": logs,
            "total_lines": total_lines,
            "from_line": from_line,
            "has_more": False,
        }


class ArticleAgent:
    """轻量级文章生成 Agent"""

    AUDIENCE_LABELS = {
        "general": "普通大众",
        "patient": "患者及家属",
        "professional": "医护同行",
    }

    TONE_LABELS = {
        "popular": "通俗易懂",
        "professional": "专业严谨",
    }

    def __init__(
        self,
        article_id: str,
        form_data: Dict[str, Any],
        task_id: Optional[str] = None,
        llm_client: Optional[LLMClient] = None
    ):
        self.article_id = article_id
        self.task_id = task_id
        self.form_data = self._normalize_form_data(form_data)
        self.llm = llm_client or LLMClient()
        self.logger = ArticleLogger(article_id)
        self.task_manager = TaskManager()

    @staticmethod
    def create_article_id() -> str:
        return f"article_{uuid.uuid4().hex[:12]}"

    def run(self) -> None:
        started_at = time.time()
        completed_titles: List[str] = []

        try:
            self._update_task(TaskStatus.PROCESSING, 1, "文章任务已启动")
            self.logger.log(
                action="article_start",
                stage="pending",
                details={
                    "form_data": self.form_data,
                    "message": "文章生成任务开始",
                },
            )

            ArticleManager.update_article(self.article_id, status="planning")
            ArticleManager.update_progress(
                self.article_id,
                status="planning",
                progress=5,
                message="开始规划文章大纲",
            )
            self._update_task(TaskStatus.PROCESSING, 5, "开始规划文章大纲")
            self.logger.log("planning_start", "planning", {"message": "开始规划文章大纲"})

            outline = self._plan_outline()
            ArticleManager.save_outline(self.article_id, outline)
            ArticleManager.update_progress(
                self.article_id,
                status="planning",
                progress=15,
                message=f"大纲规划完成，共 {len(outline['sections'])} 个章节",
            )
            self._update_task(TaskStatus.PROCESSING, 15, "大纲规划完成")
            self.logger.log(
                "planning_complete",
                "planning",
                {
                    "message": "大纲规划完成",
                    "outline": outline,
                },
            )

            sections_content: Dict[str, Dict[str, str]] = {}
            total_sections = max(1, len(outline["sections"]))

            for index, section in enumerate(outline["sections"]):
                section_title = section["title"]
                self.logger.log(
                    "section_start",
                    "generating",
                    {"message": f"开始生成章节: {section_title}"},
                    section_title=section_title,
                    section_index=index,
                )
                ArticleManager.update_progress(
                    self.article_id,
                    status="generating",
                    progress=max(15, int(15 + (index / total_sections) * 75)),
                    message=f"正在生成章节: {section_title}",
                    current_section=section_title,
                    completed_sections=completed_titles,
                )
                self._update_task(
                    TaskStatus.PROCESSING,
                    max(15, int(15 + (index / total_sections) * 75)),
                    f"正在生成章节: {section_title}",
                )

                content = self._generate_section(section, outline, sections_content)
                sections_content[str(index)] = {
                    "title": section_title,
                    "content": content,
                }
                ArticleManager.save_section(self.article_id, index, section_title, content)
                completed_titles.append(section_title)
                self.logger.log(
                    "section_complete",
                    "generating",
                    {
                        "message": f"章节 {section_title} 生成完成",
                        "content": content,
                        "content_length": len(content),
                    },
                    section_title=section_title,
                    section_index=index,
                )

                progress = int(15 + ((index + 1) / total_sections) * 80)
                ArticleManager.update_progress(
                    self.article_id,
                    status="generating",
                    progress=progress,
                    message=f"已完成章节: {section_title}",
                    current_section=section_title,
                    completed_sections=completed_titles,
                )
                self._update_task(TaskStatus.PROCESSING, progress, f"已完成章节: {section_title}")

            full_markdown = self._assemble_full_markdown(outline, sections_content)
            ArticleManager.complete_article(self.article_id, full_markdown)
            ArticleManager.update_progress(
                self.article_id,
                status="completed",
                progress=100,
                message="文章生成完成",
                completed_sections=completed_titles,
            )
            total_time_seconds = round(time.time() - started_at, 2)
            self.logger.log(
                "report_complete",
                "completed",
                {
                    "message": "文章生成完成",
                    "total_sections": len(outline["sections"]),
                    "total_time_seconds": total_time_seconds,
                },
            )
            self.task_manager.complete_task(
                self.task_id,
                {
                    "article_id": self.article_id,
                    "outline": outline,
                    "total_sections": len(outline["sections"]),
                },
            )
        except Exception as exc:
            error_message = str(exc)
            logger.exception("文章生成失败: %s", error_message)
            ArticleManager.fail_article(self.article_id, error_message)
            ArticleManager.update_progress(
                self.article_id,
                status="failed",
                progress=100,
                message="文章生成失败",
                completed_sections=completed_titles,
                error=error_message,
            )
            self.logger.log(
                "error",
                "failed",
                {
                    "message": "文章生成失败",
                    "error": error_message,
                },
            )
            if self.task_id:
                self.task_manager.fail_task(self.task_id, error_message)

    def chat(self, message: str, chat_history: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        meta = ArticleManager.get_article(self.article_id)
        if not meta:
            raise FileNotFoundError(f"文章不存在: {self.article_id}")

        article_content = meta.get("markdown_content") or self._assemble_from_meta(meta)
        if not article_content:
            raise ValueError("文章内容尚未生成，暂时无法进入深度互动")

        system_prompt = (
            "你是医学科普文章的作者助理。请仅基于给定文章内容和医学常识回答用户问题。"
            "回答要准确、克制、实用，不要编造指南或数据。如果用户要求改写，请直接给出修改建议或替代段落。"
            "避免把回答说成最终诊疗意见，必要时提醒咨询专业医生。"
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {
                "role": "system",
                "content": f"文章上下文如下：\n\n{article_content[:15000]}",
            },
        ]

        for item in (chat_history or [])[-10:]:
            role = item.get("role")
            content = (item.get("content") or "").strip()
            if role in {"user", "assistant"} and content:
                messages.append({"role": role, "content": content[:4000]})

        messages.append({"role": "user", "content": message})
        response = self.llm.chat(messages=messages, temperature=0.5, max_tokens=2048)
        return {"response": response}

    def _normalize_form_data(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        department = (form_data.get("department") or "").strip()
        department_custom = (form_data.get("departmentCustom") or "").strip()
        if department == "其他" and department_custom:
            department = department_custom

        audience_value = form_data.get("audience") or "general"
        tone_value = form_data.get("tone") or "popular"

        normalized = {
            "topic": (form_data.get("topic") or "").strip(),
            "department": department or "医学相关科室",
            "audience": audience_value,
            "audience_label": self.AUDIENCE_LABELS.get(audience_value, "普通大众"),
            "tone": tone_value,
            "tone_label": self.TONE_LABELS.get(tone_value, "通俗易懂"),
            "wordCount": int(form_data.get("wordCount") or 1500),
            "referenceMaterials": form_data.get("referenceMaterials") or [],
        }
        return normalized

    def _determine_section_count(self) -> int:
        word_count = self.form_data["wordCount"]
        if word_count <= 1200:
            return 4
        if word_count <= 2200:
            return 5
        if word_count <= 3200:
            return 6
        return 7

    def _plan_outline(self) -> Dict[str, Any]:
        section_count = self._determine_section_count()
        materials = self.form_data.get("referenceMaterials") or []
        materials_text = "、".join(materials[:8]) if materials else "无"

        messages = [
            {
                "role": "system",
                "content": (
                    "你是资深医学科普作家。请根据用户给定的创作参数，输出严格 JSON。"
                    "JSON 结构必须是："
                    '{"title":"文章标题","summary":"100字内摘要","sections":[{"title":"章节标题","description":"章节说明"}]}.'
                    "sections 长度必须等于用户要求的章节数，标题要清晰，适合逐段扩写。"
                ),
            },
            {
                "role": "user",
                "content": (
                    f"科室领域：{self.form_data['department']}\n"
                    f"科普主题：{self.form_data['topic']}\n"
                    f"目标读者：{self.form_data['audience_label']}\n"
                    f"文章调性：{self.form_data['tone_label']}\n"
                    f"期望字数：{self.form_data['wordCount']} 字\n"
                    f"参考材料：{materials_text}\n"
                    f"请规划 {section_count} 个章节的大纲，输出必须是 JSON。"
                ),
            },
        ]

        data = self._chat_json_with_fallback(messages)
        return self._normalize_outline(data, section_count)

    def _generate_section(
        self,
        section: Dict[str, str],
        outline: Dict[str, Any],
        sections_content: Dict[str, Dict[str, str]]
    ) -> str:
        previous_content = "\n\n".join(
            f"{item['title']}\n{item['content']}" for item in sections_content.values()
        )[-4000:]
        per_section_words = max(250, int(self.form_data["wordCount"] / max(1, len(outline["sections"])) ))

        messages = [
            {
                "role": "system",
                "content": (
                    "你是医学科普文章作者。请根据大纲和前文续写当前章节。"
                    "输出纯 markdown 内容，不要再写章节标题，不要输出解释性前言。"
                    "如果主题涉及风险、用药或诊疗建议，要保持审慎，避免夸大。"
                ),
            },
            {
                "role": "user",
                "content": (
                    f"文章标题：{outline['title']}\n"
                    f"文章摘要：{outline['summary']}\n"
                    f"目标读者：{self.form_data['audience_label']}\n"
                    f"文章调性：{self.form_data['tone_label']}\n"
                    f"科室领域：{self.form_data['department']}\n"
                    f"完整大纲：{json.dumps(outline['sections'], ensure_ascii=False)}\n"
                    f"前文内容（如有）：{previous_content or '无'}\n"
                    f"当前章节标题：{section['title']}\n"
                    f"当前章节说明：{section.get('description', '')}\n"
                    f"目标字数：约 {per_section_words} 字\n"
                    "请直接输出 markdown 正文。"
                ),
            },
        ]

        response = self.llm.chat(messages=messages, temperature=0.5, max_tokens=2200)
        return response.strip()

    def _assemble_full_markdown(
        self,
        outline: Dict[str, Any],
        sections_content: Dict[str, Dict[str, str]]
    ) -> str:
        parts = [f"# {outline['title']}", "", outline["summary"], ""]
        for index, section in enumerate(outline["sections"]):
            key = str(index)
            section_data = sections_content.get(key, {})
            parts.append(f"## {section['title']}")
            parts.append("")
            parts.append(section_data.get("content", ""))
            parts.append("")
        return "\n".join(parts).strip()

    def _assemble_from_meta(self, meta: Dict[str, Any]) -> str:
        outline = meta.get("outline")
        generated_sections = meta.get("generated_sections") or {}
        if not outline:
            return ""
        return self._assemble_full_markdown(outline, generated_sections)

    def _normalize_outline(self, data: Dict[str, Any], section_count: int) -> Dict[str, Any]:
        title = (data.get("title") or self.form_data["topic"]).strip()
        summary = (data.get("summary") or f"围绕 {self.form_data['topic']} 的医学科普文章。").strip()
        sections_raw = data.get("sections")
        if not isinstance(sections_raw, list):
            raise ValueError("大纲缺少 sections 列表")

        normalized_sections = []
        for item in sections_raw:
            if not isinstance(item, dict):
                continue
            title_text = (item.get("title") or "").strip()
            if not title_text:
                continue
            normalized_sections.append({
                "title": title_text,
                "description": (item.get("description") or "").strip(),
            })

        if len(normalized_sections) < section_count:
            fallback_titles = [
                "引言与背景",
                "核心知识解析",
                "高危因素与识别",
                "日常管理建议",
                "常见误区提醒",
                "何时就医",
                "总结与建议",
            ]
            for fallback_title in fallback_titles:
                if len(normalized_sections) >= section_count:
                    break
                if fallback_title in {section["title"] for section in normalized_sections}:
                    continue
                normalized_sections.append({
                    "title": fallback_title,
                    "description": "",
                })

        normalized_sections = normalized_sections[:section_count]
        return {
            "title": title,
            "summary": summary,
            "sections": normalized_sections,
        }

    def _chat_json_with_fallback(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        try:
            return self.llm.chat_json(messages=messages, temperature=0.3, max_tokens=1800)
        except Exception:
            fallback_response = self.llm.chat(
                messages=messages + [{
                    "role": "system",
                    "content": "再次提醒：输出必须是合法 JSON，不要带 markdown 代码块。"
                }],
                temperature=0.3,
                max_tokens=1800,
            )
            return self._extract_json(fallback_response)

    def _extract_json(self, text: str) -> Dict[str, Any]:
        cleaned = text.strip()
        cleaned = re.sub(r'^```(?:json)?\s*', '', cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r'\s*```$', '', cleaned)

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            match = re.search(r'\{[\s\S]*\}', cleaned)
            if match:
                return json.loads(match.group(0))
            raise ValueError(f"无法解析 LLM 返回的 JSON: {text}")

    def _update_task(self, status: TaskStatus, progress: int, message: str) -> None:
        if not self.task_id:
            return
        self.task_manager.update_task(
            self.task_id,
            status=status,
            progress=progress,
            message=message,
            progress_detail={
                "article_id": self.article_id,
                "topic": self.form_data.get("topic"),
            },
        )
