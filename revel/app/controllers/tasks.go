package controllers

import (
	"flowdle/app/models"
	"flowdle/app/services"
	"github.com/robfig/revel"
)

type Tasks struct {
	*revel.Controller
}

func (c Tasks) Index() revel.Result {
	tasks, err := services.GetTasks(c.Session["userid"])
	if err != nil {
		return c.RenderError(err)
	}

	username := c.Session["username"]
	userimg := c.Session["userimg"]
	if username == "" {
		return c.Redirect("/")
	}

	return c.Render(tasks, username, userimg)
}

func (c Tasks) New(task models.Task) revel.Result {

	err := services.AddTask(task, c.Session["userid"])
	if err != nil {
		return c.RenderError(err)
	}

	return c.Redirect("/tasks")
}
