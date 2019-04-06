import subprocess

cmd = "pass show websites/strava.com/neomo"
result = subprocess.run(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE)
cmd = result.stdout.decode('utf-8')
print(cmd)
