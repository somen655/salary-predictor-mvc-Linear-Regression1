from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models.regression import ModelRegistry
from ..models.schemas import PredictRequestSchema

home_bp = Blueprint("home", __name__)

@home_bp.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@home_bp.route("/predict", methods=["POST"])
def form_predict():
    form = request.form.to_dict()
    # Cast expected ints
    for k in ["skills_python","skills_java","skills_aws","skills_sql"]:
        if k in form:
            try:
                form[k] = int(form[k])
            except Exception:
                form[k] = 0

    data, errors = PredictRequestSchema.validate(form)
    if errors:
        return render_template("index.html", error="; ".join(errors), form=form)

    model = ModelRegistry.get()
    yhat = int(model.predict_one(data))
    return render_template("index.html", prediction=yhat, form=form)
