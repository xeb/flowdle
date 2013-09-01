package controllers

import (
	"flowdle/app/services"
	"fmt"
	"github.com/robfig/revel"
)

type Auth struct {
	*revel.Controller
}

var (
	bucket = services.GetBucket()
)

func (c Auth) Index() revel.Result {
	tokenCache := services.NewOAuthCache(c.Session, bucket)
	r, _ := services.TryOAuth(*tokenCache, "")

	if r.Success == false {
		return c.Redirect(r.AuthURL)
	}

	c.Session["username"] = r.Account.Name
	return c.Redirect("/tasks")
}

func (c Auth) Callback() revel.Result {
	tokenCache := services.NewOAuthCache(c.Session, bucket)
	code := c.Params.Get("code")
	r, err := services.TryOAuth(tokenCache, code)
	if err != nil {
		return c.RenderText(fmt.Sprintf("%s", err))
	}

	c.Session["username"] = r.Account.Name
	c.Session["userimg"] = r.Account.Picture

	if r.Success {
		return c.Redirect("/tasks")
	}

	c.Response.Status = 401
	return c.RenderText("Unauthorized")
}

func (c Auth) Logout() revel.Result {
	bucket = services.GetBucket()
	_ = bucket.Delete(fmt.Sprintf("authtoken-%s", c.Session["userid"]))
	delete(c.Session, "userid")
	delete(c.Session, "userimg")
	delete(c.Session, "username")
	return c.Redirect("/")
}
