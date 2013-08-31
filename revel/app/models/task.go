package models

import (
	"time"
)

type Task struct {
	Id        int
	Name      string
	Created   time.Time
	Completed time.Time
	Tags      []*Tag
}

type Tag struct {
	Id   int
	Name string
}

func (task Task) RelCreated() (r string) {
	return relative(task.Created)
}

func (task Task) RelCompleted() (r string) {
	return relative(task.Completed)
}

func NewTask(id int, name string, created time.Time) (task *Task) {
	task = &Task{Id: id, Name: name, Created: created}
	return
}

func relative(dt time.Time) (r string) {
	d := time.Now().Sub(dt)

	switch {
	case d < 30*time.Second:
		r = "Seconds ago"
	case d < 30*time.Minute:
		r = "Minutes ago"
	case d < 30*time.Hour:
		r = "Hours ago"
	case d < 7*24*time.Hour:
		r = "Days ago"
	case d < 7*2*24*time.Hour:
		r = "Weeks ago"
	case d < (7*24*time.Hour)*4*2:
		r = "Months ago"
	case d < (7*24*time.Hour)*12*2:
		r = "Years ago"
	}
	return
}
