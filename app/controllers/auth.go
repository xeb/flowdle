package controllers

import (
	"github.com/xeb/flowdle/app/services"
	"fmt"
	"github.com/robfig/revel"
)

var (
	bucket  = services.GetBucket()
	rootUrl = "http://localhost:9000" // todo: auto identify?
)

type Auth struct {
	*revel.Controller
}

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

	c.Session["userid"] = r.Account.Id
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
	_ = bucket.Delete(fmt.Sprintf("authtoken-%s", c.Session["authtoken"]))
	delete(c.Session, "authtoken")
	delete(c.Session, "userid")
	delete(c.Session, "userimg")
	delete(c.Session, "username")

	url := fmt.Sprintf("https://www.google.com/accounts/Logout?continue=https://appengine.google.com/_ah/logout?continue=%s", rootUrl)
	return c.Redirect(url)
}
