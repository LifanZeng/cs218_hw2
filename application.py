from flask import Flask, render_template, url_for

import time
import os
import psutil
import json

application = Flask(__name__)
@application.route('/', methods = ['GET'])
def frontpage():
    #return "<h1>CS 218，homework 1 -- by Lifan Zeng</h1><h2>1. To indicate how busy the CPU is: <a href='http://54.241.45.161/cpu_percent'>http://54.241.45.161/cpu_percent</a></h2><h2>2. To indicate how much memory the machine has used: <a href='http://54.241.45.161/used_mem'>http://54.241.45.161/used_mem</a></h2><h2>3. To indicate how much disk space has been used: <a href='http://54.241.45.161/used_disk'>http://54.241.45.161/used_disk</a></h2><h2>4. To indicate how much bandwidth is being used: <a href='http://54.241.45.161/enx0_bandwidth'>http://54.241.45.161/enx0_bandwidth</a></h2>"
    return render_template("index.html")

@application.route('/hello/', methods = ['GET'])
def hello():
    return "<h1>Hello world!</h1>"

@application.route('/cpu_percent/', methods = ['GET'])
def show_cpu_percent():
    cpu_usage_percent = psutil.cpu_percent(interval=1, percpu=True)
    return json.dumps({'CPUs usage percentages': cpu_usage_percent})

@application.route('/used_mem/', methods = ['GET'])
def show_mem():
    mem = psutil.virtual_memory()
    total_mem = mem.total
    used_mem = mem.used
    used_percent_mem = mem.percent
    return json.dumps({'Total memory (bit)': total_mem, 'Used memory (bit)': used_mem, 'Used percent': used_percent_mem})

@application.route('/used_disk/', methods = ['GET'])
def show_disk():
    disk_usage = psutil.disk_usage('/')
    total_disk = disk_usage.total
    used_disk = disk_usage.used
    used_percent = disk_usage.percent
    return json.dumps({'Total disk (bit)': total_disk, 'Used disk (bit)': used_disk, 'Used percent': used_percent})


def get_network_usage(interface):
    # To get the interface status at the beginning
    old_counters = psutil.net_io_counters(pernic=True)[interface]

    # wait 2 second:
    time.sleep(2)

    # To get the interface status at the endvi
    new_counters = psutil.net_io_counters(pernic=True)[interface]

    # To count the average bandwidth during this second
    bytes_sent = new_counters.bytes_sent - old_counters.bytes_sent
    bytes_recv = new_counters.bytes_recv - old_counters.bytes_recv
    bit_sent = bytes_sent/2 * 8
    bit_recv = bytes_recv/2 * 8
    return bit_sent, bit_recv

#@application.route('/enx0_bandwidth/', methods = ['GET'])
#def show_bandwidth():
#    # To select a network interfatce, such as 'eth0' and 'wi-fi'
#    interface = 'enX0'
#    sent, recv = get_network_usage(interface)
#    return f"<h1>The enX0 bandwidth: Sent {sent} bps, Received {recv} bps.</h1>"

#@application.route('/bandwidth/', methods = ['GET'])
#def bandwidth():
#    enx0_sent, enx0_recv = get_network_usage('enX0')
#    #enx0_recv = get_network_usage('enX0').bit_recv
#    lo_sent, lo_recv = get_network_usage('lo')
#    #lo_recv = get_network_usage('lo').bit_recv
#    return json.dumps({'Band width':{'lo':{'sent(bps)': lo_sent, 'receive(bps)': lo_recv}, 'enX0':{'sent(bps)': enx0_sent, 'receive(bps)': enx0_recv}}})


@application.route('/bandwidth/', methods = ['GET'])
def bandwidth():
    enx0_sent, enx0_recv = get_network_usage('enX0')
    #enx0_recv = get_network_usage('enX0').bit_recv
    lo_sent, lo_recv = get_network_usage('lo')
    #lo_recv = get_network_usage('lo').bit_recv
    return json.dumps({'Band width':{'lo':{'sent(bps)': lo_sent, 'receive(bps)': lo_recv}, 'enX0':{'sent(bps)': enx0_sent, 'receive(bps)': enx0_recv}}})


@application.route('/net_io_counters/', methods = ['GET'])
def net_io_counters():
    nnet = psutil.net_io_counters(pernic=True)
    return f"<h1>The net information is: {nnet}</h1>"

if __name__ == '__main__':
    application.run(host= "0.0.0.0", port=5000)
