package services

import (
	"bufio"
	"fmt"
	"os"
)

func ReadConfigOrDefault(fileName, defaultVal string) string {
	val, _ := ReadConfig(fileName)
	if val == "" {
		return defaultVal
	}
	return val
}

func ReadConfig(fileName string) (string, error) {
	path := nixRoot
	exists, _ := exists(path)
	if exists == false {
		path = winRoot
	}

	fullPath := fmt.Sprintf("%s%s", path, fileName)

	file, err := os.Open(fullPath)
	if err != nil {
		return "", err
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	scanner.Scan()
	return scanner.Text(), scanner.Err()
}

func exists(path string) (bool, error) {
	_, err := os.Stat(path)
	if err == nil {
		return true, nil
	}
	if os.IsNotExist(err) {
		return false, nil
	}
	return false, err
}
