package tests

import (
	// "flowdle/app/models"
	"github.com/xeb/flowdle/app/services"
	"fmt"
	"github.com/robfig/revel"
)

type TasksTest struct {
	revel.TestSuite
}

func (t *TasksTest) Before() {
	println("Set up")
}

func (t TasksTest) TestSortOrder() {
	userid := "111161752322909787232"
	tasks, _, _ := services.GetTasks(userid, "", false) // this will connect to couchbase
	fmt.Printf("\n---------------\n\t\tSort Test\n---------------\n-Received %d tasks, they are:\n", len(tasks))

	var lastCompleted int64 = 0
	var lastCreated int64 = 0
	var completed int64 = 0
	var created int64 = 0
	for i, val := range tasks {
		completed = val.Completed.Unix()
		created = val.Created.Unix()
		et := ""
		if completed == 0 {
			et = "\t"
		}
		fmt.Printf("\t\tTasks[%d]\tCompleted: %d, %s\tCreated: %d\n", i, completed, et, created)

		if completed > 0 && lastCompleted == 0 {
			lastCompleted = completed
		} else if completed > lastCompleted {
			t.Assertf(false, fmt.Sprintf("Task[%d] has a completed of %d when lastCompleted is %d", i, completed, lastCompleted))
		} else {
			lastCompleted = completed
		}

		if created > 0 && created == 0 {
			lastCreated = created
		} else if created > lastCreated && lastCompleted > 0 && completed > 0 && completed != lastCompleted {
			fmt.Printf("lastCompleted: %d, completed: %d", lastCompleted, completed)
			t.Assertf(false, fmt.Sprintf("Task[%d] has a created of %d when lastCreated is %d", i, created, lastCreated))
		} else {
			lastCreated = created
		}
	}
}

func (t *TasksTest) After() {
	println("Tear down")
}
