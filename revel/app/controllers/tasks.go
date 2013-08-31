package controllers

import (
	"flowdle/app/models"
	// "fmt"
	"github.com/robfig/revel"
	"time"
)

type Tasks struct {
	*revel.Controller
}

func (c Tasks) Index() revel.Result {

	task1 := &models.Task{Id: 1, Name: "Take out the trash", Date: time.Now()}
	task2 := &models.Task{Id: 2, Name: "Finish this app", Date: time.Now()}
	task3 := &models.Task{Id: 3, Name: "Charge my battery", Date: time.Now()}
	task4 := &models.Task{Id: 4, Name: "Take a vacation somewhere sunny and near the ocean", Date: time.Now()}
	tasks := []*models.Task{task1, task2, task3, task4}

	// for i := 0; i < 10; i++ {
	// 	tasks = append(tasks, task)
	// }

	return c.Render(tasks)
}
