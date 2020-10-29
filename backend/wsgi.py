from app import app


if __name__ == "__main__":
    app.config.from_object(config['test'])
    app.register_blueprint(blueprint)
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', '5000'))