package controllers

import (
	"github.com/xeb/flowdle/app/models"
	"github.com/xeb/flowdle/app/services"
	"fmt"
	"github.com/robfig/revel"
)

type Tasks struct {
	*revel.Controller
}

func (c Tasks) Index(tag string) revel.Result {
	tasks, tags, _ := services.GetTasks(c.Session["userid"], tag, false)

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

func (c Tasks) Complete(id int, complete bool) revel.Result {

	err := services.CompleteTask(id, complete, c.Session["userid"])
	if err != nil {
		return c.RenderText(fmt.Sprintf("%s", err))
	}

	return c.Redirect("/tasks")
}

func (c Tasks) Completed() revel.Result {
	tasks, tags, e := services.GetTasks(c.Session["userid"], "", true)
	if e != nil {
		return c.RenderText(fmt.Sprintf("%s", e))
	}
	username := c.Session["username"]
	userimg := c.Session["userimg"]

	if username == "" {
		return c.Redirect("/")
	}

	return c.Render(tasks, username, userimg, tags)
}
