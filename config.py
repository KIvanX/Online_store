from flask import Flask, render_template, request, redirect, session, flash
from database import Database
from jinja2 import Environment

app = Flask(__name__)
app.secret_key = 'fbRf43sRg4e3R3ke'
db = Database()
