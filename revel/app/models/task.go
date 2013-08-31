package models

import (
	"time"
)

type Task struct {
	Id   int
	Name string
	Date time.Time
	Tags []*Tag
}

type Tag struct {
	Id   int
	Name string
}

func (tag Task) RelativeTime() (r string) {
	d := time.Now().Sub(tag.Date)
	r = "No Idea"
	switch {
	case d < 30*time.Second:
		r = "A few seconds ago"
	case d < 30*time.Minute:
		r = "A few minutes ago"
	case d < 30*time.Hour:
		r = "A few hours ago"
	}
	return
}
