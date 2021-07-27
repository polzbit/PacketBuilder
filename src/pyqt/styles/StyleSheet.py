

def StyleSheet():
    return '''
#RedProgressBar {
    text-align: center;
}
#RedProgressBar::chunk {
    background-color: #F44336;
}
#GreenProgressBar {
    min-height: 12px;
    max-height: 12px;
    border-radius: 6px;
}
#GreenProgressBar::chunk {
    border-radius: 6px;
    background-color: #009688;
}
#LightBlueProgressBar {
    min-height: 12px;
    max-height: 12px;
    border-radius: 6px;
}
#LightBlueProgressBar::chunk {
    border-radius: 6px;
    background-color: #3399FF;
}
#BlueProgressBar {
    border: 2px solid #2196F3;
    border-radius: 5px;
    background-color: #E0E0E0;
}
#BlueProgressBar::chunk {
    background-color: #2196F3;
    width: 10px; 
    margin: 0.5px;
}
#pkt_lbl {
    margin-right: 10px;
}
#collapse {
    background-color: #E5E5E5;
}
#collapse_btn {
    border: none;
    border-bottom: 1px solid silver;
    background-color: #b5b5b5;
    color: #FFFFFF;
    padding-left: 30px;
    font-size: 16px;
}
#collapse_row {
    background-color: #E5E5E5;
}
#pkt_input {
    background: #FFFFFF;
}
#rule_lbl {
    margin-right: 10px;
}
#header {
    font: bold;
    border: 1px solid silver;
    border-radius: 6px;
    padding-bottom: 5px;
    margin: 5px;
}

#header::title {
    subcontrol-origin: margin;
    left: 40%;
    padding: 0px 5px 0px 5px;
}
#settings_in {
    border-bottom-width: 1px;
    border-bottom-style: solid;
    border-radius: 0px;
    border-color: silver;
    font-size: 10px;
    padding-top: 15px;
}
#tasks_btns{
    border: none;
}
#first_row_group {
    border-bottom-width: 1px;
    border-bottom-style: solid;
    border-radius: 0px;
    border-color: silver;
    padding: 15px;
}

'''