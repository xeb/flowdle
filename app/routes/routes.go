// GENERATED CODE - DO NOT EDIT
package routes

import "github.com/revel/revel"


type tApp struct {}
var App tApp


func (_ tApp) Index(
		) string {
	args := make(map[string]string)
	
	return revel.MainRouter.Reverse("App.Index", args).Url
}


type tAuth struct {}
var Auth tAuth


func (_ tAuth) Index(
		) string {
	args := make(map[string]string)
	
	return revel.MainRouter.Reverse("Auth.Index", args).Url
}

func (_ tAuth) Callback(
		) string {
	args := make(map[string]string)
	
	return revel.MainRouter.Reverse("Auth.Callback", args).Url
}

func (_ tAuth) Logout(
		) string {
	args := make(map[string]string)
	
	return revel.MainRouter.Reverse("Auth.Logout", args).Url
}


type tHome struct {}
var Home tHome


func (_ tHome) Index(
		) string {
	args := make(map[string]string)
	
	return revel.MainRouter.Reverse("Home.Index", args).Url
}


type tTasks struct {}
var Tasks tTasks


func (_ tTasks) Index(
		tag string,
		) string {
	args := make(map[string]string)
	
	revel.Unbind(args, "tag", tag)
	return revel.MainRouter.Reverse("Tasks.Index", args).Url
}

func (_ tTasks) New(
		task interface{},
		) string {
	args := make(map[string]string)
	
	revel.Unbind(args, "task", task)
	return revel.MainRouter.Reverse("Tasks.New", args).Url
}

func (_ tTasks) Complete(
		id int,
		complete bool,
		) string {
	args := make(map[string]string)
	
	revel.Unbind(args, "id", id)
	revel.Unbind(args, "complete", complete)
	return revel.MainRouter.Reverse("Tasks.Complete", args).Url
}

func (_ tTasks) Completed(
		) string {
	args := make(map[string]string)
	
	return revel.MainRouter.Reverse("Tasks.Completed", args).Url
}


type tTestRunner struct {}
var TestRunner tTestRunner


func (_ tTestRunner) Index(
		) string {
	args := make(map[string]string)
	
	return revel.MainRouter.Reverse("TestRunner.Index", args).Url
}

func (_ tTestRunner) Run(
		suite string,
		test string,
		) string {
	args := make(map[string]string)
	
	revel.Unbind(args, "suite", suite)
	revel.Unbind(args, "test", test)
	return revel.MainRouter.Reverse("TestRunner.Run", args).Url
}

func (_ tTestRunner) List(
		) string {
	args := make(map[string]string)
	
	return revel.MainRouter.Reverse("TestRunner.List", args).Url
}


type tStatic struct {}
var Static tStatic


func (_ tStatic) Serve(
		prefix string,
		filepath string,
		) string {
	args := make(map[string]string)
	
	revel.Unbind(args, "prefix", prefix)
	revel.Unbind(args, "filepath", filepath)
	return revel.MainRouter.Reverse("Static.Serve", args).Url
}

func (_ tStatic) ServeModule(
		moduleName string,
		prefix string,
		filepath string,
		) string {
	args := make(map[string]string)
	
	revel.Unbind(args, "moduleName", moduleName)
	revel.Unbind(args, "prefix", prefix)
	revel.Unbind(args, "filepath", filepath)
	return revel.MainRouter.Reverse("Static.ServeModule", args).Url
}


