package services

import (
	"errors"
	"flowdle/app/models"
	"fmt"
	"math/rand"
	"sort"
	"strings"
	"time"
)

func GetTasks(userid, tag string) (tasks models.Tasks, tags []string, err error) {
	accountKey := getAccountKey(userid)
	bucket := GetBucket()

	var accountTasks models.AccountTasks
	err = bucket.Get(accountKey, &accountTasks)
	if err != nil {
		return nil, nil, err
	}

	tasks = accountTasks.Tasks

	tags = make([]string, 0)
	for _, task := range accountTasks.Tasks {
		etags := strings.Split(task.TagString, ",")
		for _, tag := range etags {
			inlist := false
			for _, et := range tags {
				if tag == et {
					inlist = true
					continue
				}
			}

			if inlist == false && tag != "" {
				tags = append(tags, tag)
			}
		}
	}

	if tag != "" {
		tasks = make([]*models.Task, 0)
		for _, task := range accountTasks.Tasks {
			if strings.Contains(task.TagString, tag+",") {
				tasks = append(tasks, task)
			}
		}
	}

	sort.Sort(tasks)
	sort.Strings(tags)

	return
}

func CompleteTask(id int, complete bool, userid string) (err error) {
	accountKey := getAccountKey(userid)
	bucket := GetBucket()

	var accountTasks models.AccountTasks
	err = bucket.Get(accountKey, &accountTasks)
	if err != nil {
		return err
	}

	for _, task := range accountTasks.Tasks {
		if task.Id == id {
			if complete == false {
				task.Completed = time.Unix(0, 0)
			} else {
				task.Completed = time.Now()
			}
			return bucket.Set(accountKey, -1, accountTasks)
		}
	}
	return errors.New("No key found")
}

func AddTask(task models.Task, userid string) (err error) {
	accountKey := getAccountKey(userid)
	bucket := GetBucket()
	rand.Seed(time.Now().Unix())
	task.Created = time.Now()
	task.TagString = task.TagString + "," // helpful for searching
	task.Id = rand.Int()

	var accountTasks models.AccountTasks
	_ = bucket.Get(accountKey, &accountTasks)
	if accountTasks.Tasks != nil {
		accountTasks.Tasks = append(accountTasks.Tasks, &task)
	} else {
		accountTasks = models.AccountTasks{
			Id:    userid,
			Tasks: make([]*models.Task, 1),
		}

		accountTasks.Tasks[0] = &task
	}

	return bucket.Set(accountKey, -1, accountTasks)
}

func getAccountKey(userid string) (accountKey string) {
	accountKey = fmt.Sprintf("tasks-%s", userid)
	return
}
