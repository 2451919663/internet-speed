import tkinter as tk
import psutil

upload_text='上传速度:{:.2f} {}/s'
download_text='下载速度:{:.2f} {}/s'
last_upload_data=0
last_download_data=0
first=True


tou_ming_du=0.75
app=tk.Tk()
app.title(u'网速监控')#窗口名
app.geometry("140x35+1390+788")
app.attributes("-alpha",tou_ming_du)#窗体透明度
app.overrideredirect(True)#删除标题栏
app.attributes("-topmost",1)#让窗口保持置顶
#
app.config(bg = 'white')#设置背景色，少了不行
app.wm_attributes('-transparentcolor','white')#将背景色变透明

#以下这段代码实现无标题可移动和关闭窗口
def MouseDown(event):  # 不要忘记写参数event
    global mousX  # 全局变量，鼠标在窗体内的x坐标
    global mousY  # 全局变量，鼠标在窗体内的y坐标

    mousX = event.x  # 获取鼠标相对于窗体左上角的X坐标
    mousY = event.y  # 获取鼠标相对于窗左上角体的Y坐标


def MouseMove(event):
    app.geometry(f'+{event.x_root - mousX}+{event.y_root - mousY}')  # 窗体移动代码
    # event.x_root 为窗体相对于屏幕左上角的X坐标
    # event.y_root 为窗体相对于屏幕左上角的Y坐标


def exit(event):
    app.destroy()#关闭程序

#鼠标滚轮事件处理函数
def onMousewhee1(event) :
    global tou_ming_du
    if event.delta > 0:

        if tou_ming_du<=1:
            tou_ming_du += 0.05
            app.attributes("-alpha",tou_ming_du)#窗体透明度

    else:

        if tou_ming_du>=0.1:
            tou_ming_du -= 0.05
            app.attributes("-alpha", tou_ming_du)  # 窗体透明度



app.bind("<Button-1>",MouseDown)  # 按下鼠标左键绑定MouseDown函数
app.bind("<B1-Motion>",MouseMove)  # 鼠标左键按住拖曳事件,3个函数都不要忘记函数写参数
app.bind("<Double-Button-1>",exit)  # 双击鼠标左键，关闭窗体
app.bind("<MouseWheel>", onMousewhee1)#滚轮透明度
"""其中，app是Tkinter应用程序对象的名称，"<MouseWheel>"是表示鼠标滚轮事件的字符串
，onMousewhee1是用于处理鼠标滚轮事件的函数名。当用户在应用程序中使用鼠标滚轮时，会触发这个事件
，并且调用MouseScroll函数进行处理。
可以在onMousewhee1函数中定义相应的操作和响应逻辑，比如更新应用程序的状态，执行某些操作等。"""







def update_speed():
    global last_upload_data
    global last_download_data
    global first
    if first:
        first=False
        last_download_data=psutil.net_io_counters().bytes_recv#返回的是自系统启动以来系统网络接口收到字节的数量，即从其他设备发送到本机的字节数。
        last_upload_data=psutil.net_io_counters().bytes_sent#自系统启动以来发送到网络的字节数
        label1.config(text=upload_text.format(0,'kb'))
        label2.config(text=download_text.format(0,'kb'))

    else:

        cur_download_data=psutil.net_io_counters().bytes_recv
        cur_upload_data=psutil.net_io_counters().bytes_sent
        if (cur_download_data - last_download_data) / 1024 >=1024:#(cur_download_data - last_download_data)：现在的下载字节-上一秒的下载字节为每秒的速度
            label2.config(text=download_text.format((cur_download_data - last_download_data) / (1024*1024),'Mb'))
        else:
            label2.config(text=download_text.format((cur_download_data-last_download_data)/1024,'kb'))
        if (cur_upload_data - last_upload_data) / 1024 >= 1024:
            label1.config(text=upload_text.format((cur_upload_data - last_upload_data) / (1024 * 1024), 'Mb'))
        else:
            label1.config(text=upload_text.format((cur_upload_data - last_upload_data) / 1024, 'kb'))
        last_download_data=cur_download_data
        last_upload_data=cur_upload_data


    app.after(1000,update_speed)#递归


label1=tk.Label(text=upload_text.format(0,'kb'),font=('hei',10))#font是设置字体
label1.pack(fill=tk.X,expand=True)
label2=tk.Label(text=download_text.format(0,'kb'),font=('hei',10))
label2.pack(fill=tk.X,expand=True)
app.after(1000,update_speed)

app.mainloop()
