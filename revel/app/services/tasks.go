package services

import (
	"flowdle/app/models"
	"fmt"
	"math/rand"
	"sort"
	"strings"
	"time"
)

func GetTasks(userid, tag string) (tasks []*models.Task, tags []string, err error) {
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

			if inlist == false {
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

	sort.Sort(accountTasks.Tasks)
	sort.Strings(tags)

	return
}

func AddTask(task models.Task, userid string) (err error) {
	accountKey := getAccountKey(userid)
	bucket := GetBucket()

	task.Created = time.Now()
	task.TagString = task.TagString + "," // helpful for searching
	task.Id = rand.Int63()

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
