from database_models import *

all_data = db.session.query(SessionDataModel).all()
sessdt = get_session_by_index(len(all_data)-1)

architecture = []
for i in range(4):
    architecture.append(list(request.form[f'list_architecture{i}']))
sessdt.initiating_event = request.form['initiating event']
sessdt.consequence_value = 2


list_of_events = []
for i in range(4):
    list_of_events.append(request.form[f'event{i}'])
sessdt.consequence = list_of_events[len(list_of_events)-1]

frequency_of_events = []
for i in range(4):
    frequency_of_events.append(float(request.form[f'event_value{i}']))
list_of_events_and_values = []
for i in range(len(list_of_events)):
    list_of_events_and_values.append((list_of_events[i],frequency_of_events[i]))

sessdt.event_tree_probability = 0.001
print(sessdt) 

db.session.commit()


class EventTree():
    
    def __init__(self,list_of_events,hazardous_event,path_architecture):
        
        list_of_events : list
        hazardous_event : list
        path_architecture : list 
        
        self.list_of_events = list_of_events, 
        self.hazardous_event = hazardous_event, 
        self.path_architecture = path_architecture
        self.event_tree_values = self.add_events()
    
    def __repr__(self):
        return  f'''
        Event Tree (
        {self.event_tree_values[0]},
        {self.event_tree_values[1]},
        {self.event_tree_values[2]},
        {self.event_tree_values[3]}
    )
    '''
    def add_events(self):
        outcomes_list = []
        for i in range(5):
            outcomes_list.append([])

        for i in range(len(outcomes_list)):
            for path in self.path_architecture: 
                for event in path:
                    for j in range(len(self.list_of_events[0])-1):
                        if event == '1':
                            outcomes_list[i].append(self.hazardous_event[0][1]*self.list_of_events[0][j][1])
                        else:
                            print(self.hazardous_event)
                            print(path)
                            outcomes_list[i].append(self.hazardous_event[0][1]*(1 - self.list_of_events[0][j][1]))
        self.event_tree_values = outcomes_list
        return outcomes_list


def check_frequency(fx):
    if fx < 1/10000:
        frequency = 1
    if fx > 1/10000 and fx < 1/1000:
        frequency = 2
    if fx > 1/1000 and fx < 1/100:
        frequency = 3
    if fx > 1/100 and fx < 1/10:
        frequency = 4
    if fx > 1/10 and fx < 1:
        frequency = 5
    return frequency

def calculate_risk(consequence_value, frequency):
    x = check_frequency(frequency)
    risk = consequence_value + x
    return risk

def analysis_summary(event_tree_probability):
    db.create_all()
    all_data = db.session.query(SessionDataModel).all()
    session_data = get_session_by_index(len(all_data)-1)
    # consequence value is set to 2 automaitically
    risk = calculate_risk(session_data.consequence_value, event_tree_probability)
    data = {
        'Deviation': ['No flow',''],
        'Cause': [session_data.initiating_event, ''],
        'Consequence': [session_data.consequence, ''],
        'Safeguargs': ['', ''],
        'Unmitigated Risk': [risk, ''],
        'Mitigated Risk': ['', '']
    }

    df = pd.DataFrame(data)
    df.to_html('Hazop.html')

    hazop_file = open('Hazop.html', 'r')
    hazop_content = hazop_file.read()
    hazop_file.close
    output_file = open('output.txt', 'w')
    output_file.write("{% extends 'base.html' %}\n")
    output_file.write("{% block title %}Response Page{% endblock %}\n")
    output_file.write("{% block content %}\n")
    output_file.write("<h2><strong>Hazop Table</strong></h2>\n")
    output_file.write(f"{hazop_content}\n")
    output_file.write("<hr/>\n") 
    output_file.write("{% endblock %}\n")
    output_file.close()   

    output_text_file = open('output.txt', 'r')
    output_text_file_content = output_text_file.read()
    output_text_file.close()

    output_file = open(r'templates\data_analysis2.html', 'w')
    output_file.write(f'{output_text_file_content}')
    output_file.close()

db.create_all()
all_data = db.session.query(SessionDataModel).all()
print(all_data)
session_data = get_session_by_index(len(all_data)-1)

#architecture
session_value = architecture

list_architecture0 = session_value[0]
list_architecture1 = session_value[1]
list_architecture2 = session_value[2]
list_architecture3 = session_value[3]
event_tree_probability = list_of_events_and_values#list_of_events

list_of_event = []
for i in range(len(event_tree_probability)):
    list_of_event.append(event_tree_probability[i])

hazardous_event = [session_data.initiating_event,0.1]
path_architecture = [
    list_architecture0,
    list_architecture1,
    list_architecture2,
    list_architecture3
]

event3 = EventTree(list_of_event,hazardous_event,path_architecture)
x = event3.add_events()
print(x)
print(x[len(x)-1][0])# check if this works or where the actual output is located
print(event3)  
session_data.event_tree_probability = x[len(x)-1][0]
db.session.commit()
analysis_summary(x[len(x)-1][0])
