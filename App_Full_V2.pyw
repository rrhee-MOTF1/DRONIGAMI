from flask import Flask, request, render_template, url_for, flash, redirect
from datetime import datetime as dt
import os
import pandas

print("DO NOT CLOSE THIS WINDOW. DRONIGAMI IS IN DEV BUILD. THIS WINDOW MEANS THAT THE PROGRAM IS RUNNING. MINIMIZE THIS WINDOW.")

date = dt.now().strftime("%Y%m%d")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'EqIc+h}C}d.7V%t~=6Rc?xjCB&z;EIrwgS^YWn%046HP~~3@SW/}nELH{G`pyS'

########INIT########
####################
@app.route('/init')
def create_root():
    ret_url1 = request.args.get('ret_url1')
    ret_url2 = request.args.get('ret_url2')
    ret_url3 = request.args.get('ret_url3')
    if os.path.isdir(r"C:/DSAR_Data") == True:
        check1 = '0'
    else:
        os.mkdir(r"C:/DSAR_Data")
        check1 = '1'
####################
    if check1 == '0':
        ret_str1 = 'Root folder (C:/DSAR_Data) exists'
    else:
        ret_str1 = 'Root folder (C:/DSAR_Data) created'
####################
    if ret_url1 != None:
        ret_str3 = '<a href={}&{}&{}>Click here to return to mission page</a>'.format(ret_url1, ret_url2, ret_url3)
    else:
        ret_str3 = 'No further actions available. This window can be closed'
    return render_template("TemplateMain.html",
                           ret_txt='{}.'.format(ret_str1),
                           act_txt=ret_str3)
####################
####################

#######MISSION######
####################
@app.route('/mission')
def access_param():
    daily_root = r"C:/DSAR_Data/"
    incid = request.args.get('incid')
    team = request.args.get('team')
    cv = request.args.get('cv')
    if os.path.isdir(daily_root):
        mission = str(cv)[0:4]
        squad = str(cv)[5:9]
        fold_str = str(cv)[10:13]
        opt_list_code = []
        opt_list_name = []
        with open(r"C:\Users\rrhee\Desktop\DSAR_Local_Tools\Structure_List.csv") as csv:
            reader = pandas.read_csv(csv)
            for i in range(len(reader)):
                code = str(reader.values[i][0])
                if fold_str == code:
                    str_code = reader.values[i][2]
                    mtype = code[0]
                    for o in range(len(reader)):
                        if mtype == str(reader.values[o][0])[0]:
                            opt_list_code.append(reader.values[o][0])
                            opt_list_name.append(reader.values[o][3])                                            
        try:
            fold_name = incid + "_" + team + "_" + mission + "_" + squad + "_" + str_code
        except:
            fold_name = incid + "_" + team + "_" + mission + "_" + squad + "_NAN"
        mission_fold = daily_root+ '/' + fold_name
    else:
        ret_url1 = request.path + '?incid=' + incid
        ret_url2 = 'team=' + team
        ret_url3 = 'cv=' + cv
        return render_template("TemplateMain.html",
                               ret_txt='No root directory detected.',
                               act_txt='Before creating mission specific folders, <a href="/init?ret_url1={}&ret_url2={}&ret_url3={}">click here</a> to create root folder structure located at C:/DSAR_Data.'.format(ret_url1, ret_url2, ret_url3))
####################
    if os.path.isdir(mission_fold) == True:
        try:
            open(os.path.join(mission_fold, '_DONOTDELETE_process_track.txt'), 'x')
        except:
            pass
        check = '0'
    elif len(cv) == 13:
        os.mkdir(mission_fold)
        try:
            open(os.path.join(mission_fold, '_DONOTDELETE_process_track.txt'), 'x')
        except:
            pass
        check = '1'
    else:
        check = '2'
####################
    if check == '1':
        text_1 = '''Folder request recieved - Folder Created<br><br>
                    Incident: {}<br>
                    Team: {}<br>
                    Mission #: {}<br>
                    Squad #: {}<br>
                    Coded Mission Type: {}'''.format(incid, team, mission, squad, str_code)
        text_2 = 'Select craft from options below to create folder structure<br><br>'
        for i, option in enumerate(opt_list_code):
            text_2 += '<a href="/craft?craft={}&fold={}&incid={}&team={}&cv={}">{}</a><br>'.format(option, fold_name, incid, team, cv, opt_list_name[i])
        return render_template("TemplateMain.html",
                               ret_txt=text_1,
                               act_txt=text_2)
    elif check == '0':
        text_3 = '''Folder request recieved - Folder Already Exists<br><br>
                    Incident: {}<br>
                    Team: {}<br>
                    Mission #: {}<br>
                    Squad #: {}<br>
                    Coded Mission Type: {}'''.format(incid, team, mission, squad, str_code)
        text_4 = 'Select craft from options below to create folder structure<br><br>'
        for i, option in enumerate(opt_list_code):
            text_4 += '<a href="/craft?craft={}&fold={}&incid={}&team={}&cv={}">{}</a><br>'.format(option, fold_name, incid, team, cv, opt_list_name[i])
        return render_template("TemplateMain.html",
                               ret_txt=text_3,
                               act_txt=text_4)
    else:
        return render_template("TemplateMain.html",
                               ret_txt='No Code Value or Invalid Code Value provided. No folders created.',
                               act_txt='Please check the URL provided to you and try again. If needed, request a Radio Code for the mission and <a href="/rcent">Click Here</a> to enter the code and try again.')
####################
####################

########CRAFT#######
####################
@app.route('/craft')
def create_craft_fold():
    craft = request.args.get('craft')
    fold = request.args.get('fold')
    incid = request.args.get('incid')
    cv = request.args.get('cv')
    dupe_chk = request.args.get('dupe_chk')
    team = request.args.get('team')
    daily_root = r"C:/DSAR_Data/"
    mission_fold = daily_root + '/' + fold

    if dupe_chk == None:        
        with open(os.path.join(mission_fold, '_DONOTDELETE_process_track.txt'), 'r') as p_check:
            checklist = p_check.readlines()
            if str(incid + craft) in checklist or str(incid + craft + " \n") in checklist:
                flight_list1 = os.listdir(mission_fold)
                flight_list2 = []
                for item in flight_list1:
                    if item.endswith(".txt"):
                        pass
                    else:
                        flight_list2.append(item)
                new_flight_path = request.path
                return render_template("TemplateMain.html",
                                       ret_txt='Folders Already Exist. Current folders are listed below:<br>{}'.format(flight_list2),
                                       act_txt = '<a href="{}?craft={}&fold={}&incid={}&team={}&cv={}&dupe_chk=1">Click here</a> to add an additional flight for this craft. <a href="/mission?incid={}&team={}&cv={}">Click here</a> to return to mission assignment'.format(new_flight_path, craft, fold, incid, team, cv, incid, team, cv))
            else:
                with open(r"C:\Users\rrhee\Desktop\DSAR_Local_Tools\Structure_List.csv") as csv:
                    reader = pandas.read_csv(csv)
                    for i in range(len(reader)):
                        code = str(reader.values[i][0])
                        if craft == code:
                            fold_list = reader.values[i][1].split(';')
                path_list = []
                flightno = len(checklist)
                for i, fold in enumerate(fold_list):
                    if i == 0:
                        if flightno == 0:
                            global flightfold
                            flightfold = '/F01_' + fold
                            join_path = mission_fold + flightfold
                            path_list.append(join_path)
                        elif flightno < 10:
                            flightfold = '/F0' + str(flightno) + '_' + fold
                            join_path = mission_fold + flightfold
                            path_list.append(join_path)
                        else:
                            flightfold = '/F' + str(flightno) + '_' + fold
                            join_path = mission_fold + flightfold
                            path_list.append(join_path)
                    else:
                        join_path = mission_fold + flightfold + fold
                        path_list.append(join_path)
                for path in path_list:
                    os.mkdir(path)
                
                with open(os.path.join(mission_fold, '_DONOTDELETE_process_track.txt'), 'a') as p_track:
                    p_track.write(' \n' + incid + craft)

                return render_template("TemplateMain.html",
                               ret_txt='Folders Created.',
                               act_txt='<a href="/mission?incid={}&team={}&cv={}">Return to mission assignment</a>'.format(incid, team, cv))
            
    elif dupe_chk == '1':
        with open(os.path.join(mission_fold, '_DONOTDELETE_process_track.txt'), 'r') as p_check:
            checklist = p_check.readlines()
        with open(r"C:\Users\rrhee\Desktop\DSAR_Local_Tools\Structure_List.csv") as csv:
            reader = pandas.read_csv(csv)
            for i in range(len(reader)):
                code = str(reader.values[i][0])
                if craft == code:
                    fold_list = reader.values[i][1].split(';')
        path_list = []
        flightno = len(checklist)
        for i, fold in enumerate(fold_list):
            if i == 0:
                if flightno == 0:
                    flightfold = '/F01_' + fold
                    join_path = mission_fold + flightfold
                    path_list.append(join_path)
                elif flightno < 10:
                    flightfold = '/F0' + str(flightno) + '_' + fold
                    join_path = mission_fold + flightfold
                    path_list.append(join_path)
                else:
                    flightfold = '/F' + str(flightno) + '_' + fold
                    join_path = mission_fold + flightfold
                    path_list.append(join_path)
            else:
                join_path = mission_fold + flightfold + fold
                path_list.append(join_path)
        for path in path_list:
            os.mkdir(path)

        with open(os.path.join(mission_fold, '_DONOTDELETE_process_track.txt'), 'a') as p_track:
                    p_track.write(' \n' + incid + craft)

        return render_template("TemplateMain.html",
                           ret_txt='Folders Created.',
                           act_txt='<a href="/mission?incid={}&team={}&cv={}">Return to mission assignment</a>'.format(incid, team, cv))
####################
####################

########RCODE#######
####################
@app.route('/rcode', methods=(['GET','POST']))
def rcode_ent():
    if request.method == 'POST':
        rcp1 = request.form['param1']
        rcp2 = request.form['param2']
        rcp3 = request.form['param3']
        rcp4 = request.form['param4']
        if not rcp1:
            flash('Incident Code Required')
        elif not rcp2:
            flash('Incident Code Required')
    return render_template("RCodeForm.html")

@app.route('/stest')
def test_server():
    return render_template("TemplateMain.html",
                           ret_txt = 'Connection succesful. WGSI server operational.',
                           act_txt = 'No further actions available. This window can be closed')

@app.route('/admin/func001')
def ad_func001():
    f001_param1 = request.args.get('action')
    if os.path.isdir("C:/FStructure_Templates"):
        if f001_param1 == None:
            return render_template("TemplateMain.html",
                                   ret_txt = 'Admin Function 001 (Create/Modify/Delete folder structues). Valid template folder found. No action provided.',
                                   act_txt = '<a href="?action=help">Click here</a> for assistance')
        elif f001_param1 == 'help':
            return render_template("TemplateMain.html",
                                   ret_txt = 'Valid template folder found. See list below for valid actions.',
                                   act_txt = '''To use commands, click the command below:<br>
                                                Parameter : Description<br>
                                                delt : remove all existing folder templates from the template folder, this operation is safe to perform manually outside of the admin function 001<br>
                                                prep : prepares all existing folder templates. LOCAL DEVICE ONLY, DISTRIBUTION OF UPDATED FOLDER STRUCTURE LIST MUST BE DONE MANUALLY<br>
                                                push : modifies the LOCAL folder template database. LOCAL DEVICE ONLY, DISTRIBUTION OF UPDATED FOLDER STRUCTURE LIST MUST BE DONE MANUALLY<br>
                                                dist : provides a distributable file containing all folder templates that can be shared across devices''')

@app.route('/status', methods=(['GET', 'POST']))
def status_update():
    if request.method == 'POST':
        status = request.form['status']
    return render_template('statusForm.html')

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='127.0.0.1', port=8080)
