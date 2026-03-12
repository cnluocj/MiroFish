"""
医学科普文章 API
"""

import threading
import traceback

from flask import jsonify, request

from . import article_bp
from ..config import Config
from ..models.task import TaskManager
from ..services.article_agent import ArticleAgent, ArticleManager
from ..utils.logger import get_logger

logger = get_logger('mirofish.article_api')


def _extract_form_data(data):
    return {
        "topic": (data.get("topic") or "").strip(),
        "department": (data.get("department") or "").strip(),
        "departmentCustom": (data.get("departmentCustom") or "").strip(),
        "audience": (data.get("audience") or "general").strip(),
        "tone": (data.get("tone") or "popular").strip(),
        "wordCount": int(data.get("wordCount") or 1500),
        "referenceMaterials": data.get("referenceMaterials") or [],
    }


@article_bp.route('/generate', methods=['POST'])
def generate_article():
    try:
        if not Config.LLM_API_KEY:
            return jsonify({
                "success": False,
                "error": "LLM_API_KEY 未配置，无法启动文章生成"
            }), 400

        data = request.get_json(silent=True) or {}
        form_data = _extract_form_data(data)

        if not form_data["topic"]:
            return jsonify({"success": False, "error": "topic 不能为空"}), 400
        if not form_data["department"] and not form_data["departmentCustom"]:
            return jsonify({"success": False, "error": "department 不能为空"}), 400

        task_manager = TaskManager()
        task_id = task_manager.create_task(
            task_type="article_generate",
            metadata={
                "topic": form_data["topic"],
                "department": form_data["department"] or form_data["departmentCustom"],
            }
        )
        article_id = ArticleAgent.create_article_id()
        ArticleManager.create_article(article_id, task_id, form_data)

        def run_task():
            agent = ArticleAgent(article_id=article_id, form_data=form_data, task_id=task_id)
            agent.run()

        thread = threading.Thread(target=run_task, daemon=True)
        thread.start()

        return jsonify({
            "success": True,
            "data": {
                "task_id": task_id,
                "article_id": article_id,
                "message": "文章生成任务已启动",
            }
        })
    except Exception as exc:
        logger.error("启动文章生成失败: %s", str(exc))
        return jsonify({
            "success": False,
            "error": str(exc),
            "traceback": traceback.format_exc()
        }), 500


@article_bp.route('/<article_id>', methods=['GET'])
def get_article(article_id: str):
    try:
        article = ArticleManager.get_article(article_id)
        if not article:
            return jsonify({"success": False, "error": f"文章不存在: {article_id}"}), 404

        progress = ArticleManager.get_progress(article_id)
        return jsonify({
            "success": True,
            "data": {
                **article,
                "progress": progress,
            }
        })
    except Exception as exc:
        logger.error("获取文章失败: %s", str(exc))
        return jsonify({
            "success": False,
            "error": str(exc),
            "traceback": traceback.format_exc()
        }), 500


@article_bp.route('/<article_id>/progress', methods=['GET'])
def get_article_progress(article_id: str):
    try:
        progress = ArticleManager.get_progress(article_id)
        if not progress:
            return jsonify({"success": False, "error": f"文章进度不存在: {article_id}"}), 404

        return jsonify({
            "success": True,
            "data": progress,
        })
    except Exception as exc:
        logger.error("获取文章进度失败: %s", str(exc))
        return jsonify({
            "success": False,
            "error": str(exc),
            "traceback": traceback.format_exc()
        }), 500


@article_bp.route('/<article_id>/agent-log', methods=['GET'])
def get_article_agent_log(article_id: str):
    try:
        from_line = request.args.get('from_line', 0, type=int)
        data = ArticleManager.get_agent_log(article_id, from_line=from_line)
        return jsonify({
            "success": True,
            "data": data,
        })
    except Exception as exc:
        logger.error("获取文章日志失败: %s", str(exc))
        return jsonify({
            "success": False,
            "error": str(exc),
            "traceback": traceback.format_exc()
        }), 500


@article_bp.route('/chat', methods=['POST'])
def chat_with_article():
    try:
        if not Config.LLM_API_KEY:
            return jsonify({
                "success": False,
                "error": "LLM_API_KEY 未配置，无法进行对话"
            }), 400

        data = request.get_json(silent=True) or {}
        article_id = (data.get("article_id") or "").strip()
        message = (data.get("message") or "").strip()
        chat_history = data.get("chat_history") or []

        if not article_id:
            return jsonify({"success": False, "error": "article_id 不能为空"}), 400
        if not message:
            return jsonify({"success": False, "error": "message 不能为空"}), 400

        article = ArticleManager.get_article(article_id)
        if not article:
            return jsonify({"success": False, "error": f"文章不存在: {article_id}"}), 404

        agent = ArticleAgent(article_id=article_id, form_data=article.get("form_data") or {})
        result = agent.chat(message=message, chat_history=chat_history)

        return jsonify({
            "success": True,
            "data": result,
        })
    except Exception as exc:
        logger.error("文章对话失败: %s", str(exc))
        return jsonify({
            "success": False,
            "error": str(exc),
            "traceback": traceback.format_exc()
        }), 500
