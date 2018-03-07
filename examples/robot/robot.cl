configuration = {
	default: 
		keyword = keyword.control;
		operation = keyword.operator.new;
	comment:
		line = "#";
		block:
			start = "++";
			end = "--";
}

rules = {
	keyword:
		InitialCommand = entity.name.class;
		Direction = support.class;
}

matches = {
	"up", "wi+th", "+" = variable.language;
}

regular expressions = {
	"\\w+" = variable.language;
}