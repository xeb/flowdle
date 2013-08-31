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

	task1 := models.NewTask(1, "Take out the trash", time.Now())

	task2 := models.NewTask(2, "Finish this app", time.Now().Add(-5*12*24*time.Hour))
	task2.Completed = time.Now().Add(-2 * time.Hour)

	task3 := models.NewTask(3, "Charge my battery", time.Now().Add(-5*time.Hour))
	task4 := models.NewTask(4, "Take a vacation somewhere sunny and near the ocean", time.Now())
	task5 := models.NewTask(5, "Learn to be better at frontend development", time.Now().Add(-5*24*time.Hour))
	tasks := []*models.Task{task1, task2, task3, task4, task5}

	return c.Render(tasks)
}
