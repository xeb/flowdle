package controllers

import (
	"flowdle/app/models"
	"flowdle/app/services"
	"fmt"
	"github.com/robfig/revel"
)

type Tasks struct {
	*revel.Controller
}

func (c Tasks) Index(tag string) revel.Result {
	tasks, tags, _ := services.GetTasks(c.Session["userid"], tag)

	username := c.Session["username"]
	userimg := c.Session["userimg"]

	if username == "" {
		return c.Redirect("/")
	}

	return c.Render(tasks, username, userimg, tags, tag)
}

func (c Tasks) New(task models.Task) revel.Result {

	err := services.AddTask(task, c.Session["userid"])
	if err != nil {
		return c.RenderText(fmt.Sprintf("%s", err))
	}

	return c.Redirect("/tasks")
}
