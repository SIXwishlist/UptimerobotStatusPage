from flask import Flask, render_template

from uptimerobot.uptimerobot import UptimeRobot

app = Flask(__name__)
app.config.from_pyfile('settings.py')

page_name = app.config.get('PAGE_NAME', 'UptimeRobot')
robot = UptimeRobot(app.config['UPTIMEROBOT_API_KEY'])
status_down = ['8', '9']
status_paused = ['0', '1']


@app.route('/')
def hello():
    status, response = robot.getMonitors()
    if status:
        monitors = response['monitors']['monitor']
        monitors_formatted = []
        for monitor in monitors:
            status_raw = monitor['status']
            if status_raw in status_down:
                status = 'danger'
            elif status_raw in status_paused:
                status = 'warning'
            else:
                status = 'success'
            m = (
                monitor['id'],
                monitor['friendlyname'],
                int(float(monitor['alltimeuptimeratio'])),
                status
                )
            monitors_formatted.append(m)
        return render_template('index.html', monitors=monitors_formatted,
                               page_name=page_name)
    else:
        return 501

if __name__ == '__main__':
    app.run()
