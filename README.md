# TextX-extensions

This project enable you to create extension for Visual Studio Code, which support text coloring and/or code outline for dsl languages wirtten in textX.

## Getting Started

Create rules for coloring and store them in the file with extension **.txcl** and/or create rules for code outline and store them in the file with extension **.txol**. Then, go to *.txconfig*, and fill it appropriate. At the the, run main.py script. 

### Prerequisites
Have installed python 3, textX and jinja2

## Example
In this example we will demonstrate how to create support for **workflow** dsl language.

### Grammar
Create grammar in textX and store it in the file with exntesion **.tx**.

```
/* Simple workflow language. */

Program:
  workflow = Workflow
  init = Init
  tasks *= Task
  actions *= Action
;

Workflow:
  'workflow' name=ID desc=STRING?
;

Init:
  'init' init=[Task]
;

Task:
  'task' name=ID '{'
    ( entry=Entry | leave=Leave | next=Next )*
  '}'
;

Entry:
	'entry' entry=[Action]
;

Leave:
	'leave' leave=[Action]
;

Next:
	'next' next+=[Task][',']
;

Action:
  'action' name=ID
;

Comment:
  /\/\/.*$/
;
```

### Coloring
Create coloring rules in the file with exntesion **.txcl**.

```
configuration {
	default: 
		keyword = keyword.control;
		operation = keyword.operator;
	comment:
		line = "//";
		block:
			start = "/*";
			end = "*/";
}

rules {
	keyword:
		Workflow, Init = storage.type;
		Task = entity.name.class;
		Entry, Leave = support.variable;
		Next = storage.modifier;
		Action = storage.modifier;
	operation:
		Task = emphasis;
		Next = storage.type;
}

matches {
	"action" = meta.tag;
}
```

### Outline
Create outline rules in the file with exntesion **.txol**. 
Put your paths for the icons.

```
Workflow {
	label = name + '( ' + desc + ' )'
	icon = "C:\\Users\\Nemanja\\Desktop\\icons\\workflow.png"
}

Init {
	label = init
	icon = "*path_to_icon*"
}

Task {
	label = name
	icon = "*path_to_icon*"
}

Entry {
	label = entry
	icon = "*path_to_icon*"
}

Leave {
	label = leave
	icon = "*path_to_icon*"
}

Next {
	label = next
	icon = "*path_to_icon*"
}

Action {
	label = name
	icon = "*path_to_icon*"
}
```

### Configuration
Modify .txconfig file. 
Fill config file with appropriate data.

```
dsl workflow [wf] {
	general {
		publisher: "*publisher*"
		author: "*author*"
		version: "*version*"
    }

	paths {
		grammar: "*path_to_tx_file*"
		generation: "*path_to_existing_folder*"
		outline: "*path_to_txol_file*"
		coloring: "*path_to_txcl_file*"
	}

	python {
	    interpreter: "*path_to_python_interpreter*"
	}
}
```

* If you want to create extension only for coloring, then delete ```outline: "*path_to_txol_file*"``` and ```python { interpreter: "*path_to_python_interpreter*" }```
* If you want to create extension only for outline, then delete ```coloring: "*path_to_txcl_file*"```

## Put in action 

1. Run main.py script. 
2. You can find extension on *path_to_existing_folder* (this path is previously stored under generation section).
3. Provide exstension to be stored in folder for Visual Studio Code extensions (**.vscode**).
4. Restart Visual Studio Code.
5. Create file with extension **.wf**.

## Authors

* **Nemanja Starcev**

## License

This project is licensed under the MIT License

![alt text](https://github.com/starcev/textX-extensions/tree/master/art/workflow.png)