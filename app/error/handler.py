from flask import render_template


class ErrorPagesHandler:

    @staticmethod
    def page_forbidden(error):
        return render_template('errors/403.html', e=error), 403

    @staticmethod
    def page_not_found(error):
        return render_template('errors/404.html', e=error), 404

    @staticmethod
    def internal_server_error(error):
        return render_template('errors/500.html', e=error), 500

