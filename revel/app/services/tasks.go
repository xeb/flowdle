package services

import (
	"flowdle/app/models"
	"fmt"
	"time"
)

func GetTasks(userid string) (tasks []*models.Task, err error) {
	accountKey := getAccountKey(userid)
	bucket := GetBucket()

	var accountTasks models.AccountTasks
	err = bucket.Get(accountKey, &accountTasks)
	if err != nil {
		return nil, err
	}

	return accountTasks.Tasks, nil
}

func AddTask(task models.Task, userid string) (err error) {
	accountKey := getAccountKey(userid)
	bucket := GetBucket()

	task.Created = time.Now()
	task.TagString = task.TagString + "," // helpful for searching

	var accountTasks models.AccountTasks
	err = bucket.Get(accountKey, &accountTasks)
	if err != nil {
		return err
	}

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
