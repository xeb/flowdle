Flowdle
================
Flowdle is a task-tracking application originally built with Python on Google's App Engine in 2008.  It has laid dormant for a surperior technology to rise up & take its place.

But all the while, it has been running seamlessly on GAE, see: [http://www.flowdle.com](http://www.flowdle.com)

I've tried Wunderlist and other means to track basic "TODO" style tasks; however, I continued to use Flowdle day-after-day.  Perhaps it is narcissism, but I enjoy*ed* the app.  Therefore, this commit is the start of an ongoing attempt for me to rebuild it using [Go](http://golang.org) and [Revel](http://robfig.github.io/revel/).  

### Update ###
I've decied to stop working Flowdle as [http://todoist.com](http://todoist.com) has become my de facto task tracking app.  I love it.  It's wonderful & everything I wanted Flowdle to be.  I'll keep the repository around but this project is archived for all intents and purposes.


### Outstanding Concerns / Notes
* Rebuilding Flowdle is more about experiencing Revel and not about GAE
* Given recent experience, I'm going to use [Couchbase](http://couchbase.com) and [go-couchbase](https://github.com/couchbaselabs/go-couchbase), see some [benchmarks](http://github.com/xeb/couchbase-tests)
