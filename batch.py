from apscheduler.schedulers.background import BackgroundScheduler
def batch():
  print("Hello World!")

sched = BackgroundScheduler(standalone=True,coalesce=True)
sched.add_job(hello_world, 'interval', seconds=1)
sched.start()