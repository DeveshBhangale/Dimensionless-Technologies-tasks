from flask import * 
from flask import send_file  
app = Flask(__name__)  
 
@app.route('/')  
def upload():  
    return render_template("file_upload_form.html")  
 
@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']  
        f.save("C:/Devesh/Dimentionless Tasks/static/sample_input_dataset/{}".format(f.filename))  
        f1 = request.files['file1'] 
        f1.save("C:/Devesh/Dimentionless Tasks/static/sample_input_dataset/{}".format(f1.filename))
        
        
        import xml.etree.ElementTree as ET

        tree = ET.parse("C:/Devesh/Dimentionless Tasks/static/sample_input_dataset/{}".format(f1.filename))
        root = tree.getroot()
        global name 
        global coordinates
        name,coordinates = [],[]
        for child in root.iter('object'):
            name.append(child.find('name').text)
            coordinates.append([int(child.find('bndbox').find('xmin').text),int(child.find('bndbox').find('ymin').text)
                                ,int(child.find('bndbox').find('xmax').text),int(child.find('bndbox').find('ymax').text)])
        
        session['name']=name
        session['coordinates']= coordinates
        # Python program to explain cv2.rectangle() method
        
        # importing cv2
        import cv2
       
        # path
        #path = r("C:/Devesh/Dimentionless Tasks/static/sample_input_dataset/{}".format(f.filename))
        
        # Reading an image in default mode
        image = cv2.imread("C:/Devesh/Dimentionless Tasks/static/sample_input_dataset/{}".format(f.filename))
        
        # Window name in which image is displayed
        window_name = 'Image'
        
        # Start coordinate, here (5, 5)
        # represents the top left corner of rectangle
        start_point = (249, 215)
        
        # Ending coordinate, here (220, 220)
        # represents the bottom right corner of rectangle
        end_point = (444, 368)
        
        # Blue color in BGR
        color = (0, 0, 255)
        
        # Line thickness of 2 px
        thickness = 2
        
        # Using cv2.rectangle() method
        # Draw a rectangle with blue line borders of thickness of 2 px
        '''image = cv2.rectangle(image, start_point, end_point, color, thickness)
        cv2.putText(image, 'Gun', start_point, cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2,cv2.LINE_AA)'''
        
        for i in range(len(name)):
            image = cv2.rectangle(image,(coordinates[i][0],coordinates[i][1]),(coordinates[i][2],coordinates[i][3]),
                                  (0,0,255),2)
            cv2.putText(image, name[i], (coordinates[i][0],coordinates[i][1]), cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2,cv2.LINE_AA)
        
        cv2.imwrite("C:/Devesh/Dimentionless Tasks/static/sample_output_image/{}".format(f.filename), image)
        #cv2.imwrite("C:/Devesh/Dimentionless Tasks/static/sample_output_image/abc.jpg", image)
        # Displaying the image
        #cv2.imshow(window_name, image)
        global a
        a = "static/sample_output_image/"+str(f.filename)
        #print(a)
        return render_template("success.html",name = f.filename, img= a)  

@app.route('/download',methods=['GET'])
def download_file():
    return send_file('C:/Devesh/Dimentionless Tasks/static/abc.csv',as_attachment=True)

@app.route('/getcsv',methods=['GET','POST'])
def getcsv():
    if request.method=='POST':
        stdate = request.form.get('startdate')
        enddate = request.form.get('enddate')
        stdate = stdate.replace('-','')
        enddate = enddate.replace('-','')
        import mysql.connector
        #mydb = mysql.connector.connect(host='localhost',user='devesh',password='database' )
        mydb = mysql.connector.connect(host='localhost',user='root',password='mysql',database='dt')
        cur = mydb.cursor()
        cur.execute("CREATE DATABASE if not exists dt")
        s = 'CREATE TABLE if not exists dt(image_name varchar(100),object_name varchar(100),xmin integer(10),ymin integer(10),xmax integer(10),ymax integer(10),date DATE)'
        cur.execute(s)
        
        insert = 'INSERT INTO dt(image_name,object_name,xmin,ymin,xmax,ymax,date) VALUES(%s,%s,%s,%s,%s,%s,%s)'
        import datetime 
        name = session.get('name')
        coordinates = session.get('coordinates')
        for i in range(len(name)):
            d = datetime.datetime.now().strftime('%Y-%m-%d')
            cur.execute(insert,(str('abc'),str(name[i]),(coordinates[i][0]),(coordinates[i][1]),(coordinates[i][2]),(coordinates[i][3]),d))
        mydb.commit()
        import pandas as pd  
        imgname = []
        objname,xmin,ymin,xmax,ymax,dt1 = [],[],[],[],[],[]
        cur.execute('SELECT * from dt WHERE date BETWEEN {} AND {}'.format(stdate,enddate)) 
        res = cur.fetchall()
        
        for i in range(len(res)):
            imgname.append(res[i][0])
            objname.append(res[i][1])
            xmin.append(res[i][2])
            ymin.append(res[i][3])
            xmax.append(res[i][4])
            ymax.append(res[i][5])
            dt1.append(str(res[i][6]))
              
        df = pd.DataFrame({'Image Name': imgname, 'Object Name': objname, 'xmin':xmin,'ymin':ymin,'xmax':xmax,'ymax':ymax,'Date':dt1} ) 
            
        # saving the dataframe 
        df.to_csv('C:/Devesh/Dimentionless Tasks/static/abc.csv')
        return render_template('download.html', abc = 'C:/Devesh/Dimentionless Tasks/static/abc.csv')
    #return render_template('download.html')
if __name__ == '__main__':  
    
    app.config['SECRET_KEY'] = 'gg'
    app.run(debug = True, use_reloader=False)
    