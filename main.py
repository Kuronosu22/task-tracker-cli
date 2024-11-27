#!/usr/bin/env python3

from sys import argv
import json
from time import ctime
from operator import itemgetter as ig

def openFileInRead():
    with open(filename, "r+") as file:
            file_data = json.load(file)
            return file_data, file

def addToJson(data):
    with open(filename, "r+") as file:
        file_data = json.load(file)
        if descChecker(argv[2]):
            print("Task already in the list")
        else:
            id_list = []
            for i in file_data["tasks"]:
                for item in i.items():
                    if type(item[1]) is int:
                        id_list.append(item[1])
            id_list.sort()
            missed_id, end = missing_id(id_list)
            if missed_id == []:
                data["id"] = end + 1
                file_data["tasks"].append(data)
                file.seek(0)
                json.dump(file_data, file, indent=4)
            else:
                data["id"] = missed_id[0]
                file_data["tasks"].append(data)
                file.seek(0)
                file_data["tasks"].sort(key=ig("id"))
                json.dump(file_data, file, indent=4)

def missing_id(id_list):
    if id_list == []:
        return [], False
    start, end = 1, id_list[-1]
    missed_id = set(range(start, end + 1)).difference(id_list)
    return list(missed_id), end


def descChecker(new_desc):
    file_data, file = openFileInRead()
    return any(file_data['description'] == new_desc for file_data in file_data['tasks'])

def createJson():
    try:
        with open(filename, "x") as file:
            json.dump(body, file, indent=4)
    except FileExistsError:
        pass

def deleteJsonTask(id):
    file_data, file = openFileInRead()
    list_data = file_data.get("tasks")
    for i in range(len(list_data)):
        if list_data[i]["id"] == int(id):
            del list_data[i]
            with open(filename, "w") as file:
                json.dump(file_data, file, indent=4)
                return True

def updateJsonTask(upId, new_desc):
    with open(filename, "r+") as file:
        file_data = json.load(file)
        list_data = file_data.get("tasks")
        if descChecker(new_desc) == False:
            for item in list_data:
                if int(upId) == item["id"]:
                    item.update({f"description" : new_desc})
                    item.update({f"updatedAt" : current_time})
                    with open(filename, "w") as file:
                        json.dump(file_data, file, indent=4)
                        return True
        else:
            print("There's already a task with this description")

def markInProgress(id):
    file_data, file = openFileInRead()
    list_data = file_data.get("tasks")
    for item in list_data:
        if int(id) == item["id"]:
            if item["status"] == "in-progress":
                return False
            else:
                item.update({f"status" : "in-progress"})
                with open(filename, "w") as file:
                    json.dump(file_data, file, indent=4)
                    return True
                
def markDone(id):
    file_data, file = openFileInRead()
    list_data = file_data.get("tasks")
    for item in list_data:
        if int(id) == item["id"]:
            if item["status"] == "done":
                return False
            else:
                item.update({f"status" : "done"})
                with open(filename, "w") as file:
                    json.dump(file_data, file, indent=4)
                    return True

def listAll():
    file_data, file = openFileInRead()
    list_data = file_data.get("tasks")
    if list_data == []:
        return False
    else:
        for item in list_data:
            print(json.dumps(item, indent=4))
        return True
    

def listDone():
    file_data, file = openFileInRead()
    list_data = file_data.get("tasks")
    if list_data == []:
        return False
    else:
        for item in list_data:
            if item["status"] == "done":
                print(json.dumps(item, indent=4))
        return True
    

def listInProgress():
    file_data, file = openFileInRead()
    list_data = file_data.get("tasks")
    for item in list_data:
        if item["status"] == "in-progress":
            print(json.dumps(item, indent=4))

def listTodo():
    file_data, file = openFileInRead()
    list_data = file_data.get("tasks")
    for item in list_data:
        if item["status"] == "todo":
            print(json.dumps(item, indent=4))

def main():
    createJson()
    try:
        if argv[1] == "add":
            new_data = {
                "id" : 1, 
                "description" : argv[2],
                "status" : "todo",
                "createdAt" : current_time,
                "updatedAt" : current_time,
            }
            addToJson(new_data)
            
        elif argv[1] == "delete":
            deleteJsonTask(argv[2])

        elif argv[1] == "update":
            if not updateJsonTask(argv[2], argv[3]):
                print(f"No task with ID: {int(argv[2])}")

        elif argv[1] == "mark-in-progress":
            if markInProgress(argv[2]):
                print(f"Task with ID: {argv[2]} is now in-progress")
            else:
                print(f"Task with ID: {argv[2]} was already in-progress")

        elif argv[1] == "mark-done":
            if markDone(argv[2]):
                print(f"Task with ID: {argv[2]} is now done")
            else:
                print(f"Task with ID: {argv[2]} was already done")

        elif argv[1] == "list":
            try:
                if argv[2] == "done":
                    if listDone() == False:
                        raise EnvironmentError("No tasks")
                elif argv[2] == "in-progress":
                    if listInProgress() == False:
                        raise EnvironmentError("No tasks")
                elif argv[2] == "todo":
                    if listTodo() == False:
                        raise EnvironmentError("No tasks")
                else:
                    raise SyntaxError("Argument invalid")
            except IndexError:
                if listAll() == False:
                    raise EnvironmentError("No tasks")
        else:
            raise SyntaxError("Missing arguments")
    except SyntaxError:
        raise SyntaxError("Missing arguments")


filename = "tasks.json"

current_time = ctime() 

body = {
    "tasks" : []
}

main()