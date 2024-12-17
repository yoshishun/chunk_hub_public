from flask import Flask, render_template, redirect, url_for, request, session, jsonify
from flask import Blueprint
import re
import mysql.connector
import uuid
import string
import random
from pyvis.network import Network
from backend.models import DatabaseManager, Folder, Chunk, ChunkSentence, ChunkSentenceLink, Statistics, ChunkPronouncedCount, ChunkSentencePronouncedCount
from datetime import datetime, timedelta
from flask_login import login_user
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

from flask import request, jsonify, session
import random
import string


api = Blueprint('api', __name__)


db_mng = DatabaseManager()
db_mng.connect()


def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        print(f"Session contents: {session}")
        if 'logged_in' not in session:
            return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401
        return func(*args, **kwargs)
    return decorated_function
