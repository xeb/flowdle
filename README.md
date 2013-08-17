Flowdle
================
Flowdle is a task-tracking application originally built with Python on Google's App Engine in 2008.  It has laid dormant for a surperior technology to rise up & take its place.

I've tried Wunderlist and other means to track basic "TODO" style tasks; however, I continue to use Flowdle day-after-day.  Perhaps it is narcissism, but I enjoy the app.  Therefore, this commit is the start of an ongoing attempt for me to rebuild it using [Go](http://golang.org) and [Revel](http://robfig.github.io/revel/).  

Check back later to see my progress!


### Outstanding Concerns / Notes
* I'd like to continue using GAE, but Revel doesn't quite run on it yet.  See [Revel Issue #239](https://github.com/robfig/revel/issues/239)
* Rebuilding Flowdle is more about experiencing Revel and not about GAE
* I'm not going to worry about Authentication just yet
* Given recent experience, I'm going to use [Couchbase](http://couchbase.com) and [go-couchbase](https://github.com/couchbaselabs/go-couchbase), see some [benchmarks](http://github.com/xeb/couchbase-tests)