"""
    Web App with file based ACL.
"""
 
import os
import struct
 
from flask import Flask, request, render_template, abort, flash, redirect, url_for
 
"""
    Flask Config
"""
app = Flask(__name__)
app = Flask(__name__)
app.config['DEBUG'] = False
app.secret_key = ""
 
FLAG = '??'
 
class ACL(object):
    """
    Intent:
        ACL for the Application
 
    Responsibilities:
        - Add New Records to ACL
        - Verify existing records in ACL
 
    Data Structures
        - record
          {
              'username': <str>username[100],
              'password': <str>password[100],
              'admin': <str:`true/false`>admin
          }
    """
 
    DEFAULT_ACL_FILE = 'acl.data'
 
    def __init__(self, *args, **kwargs):
        """
        ACL(, [file_name, ])
        :param str file_name kwarg
        """
        self.acl_file = kwargs.get('acl_file', self.DEFAULT_ACL_FILE)
        self.acl_lines = self._read_acl_file()
 
    """
        Writing Methods
    """
    @staticmethod
    def _pack_data(data_dict):
        """
            Pack data with data_structure.
        """
        return '{}:{}:{}'.format(
                                    data_dict['username'],
                                    data_dict['password'],
                                    data_dict['admin']
                                )
 
    @staticmethod
    def _append_data(filename, data):
        """
            write `data` to filename as binary data.
        """
        with open(filename, 'a') as f:
            f.write(data)
            f.write('\n') # New Line Delimiter
 
    def _append_record(self, data_dict, *args, **kwargs):
        """
            Pack data and append to file.
        """
        bin_data = self._pack_data(data_dict)
 
        self._append_data(self.acl_file, bin_data)
 
    def add_record(self, username, password, admin, *args, **kwargs):
        """
            Add record to ACL.
            - Client Facing
        """
        record = {
            'username': username,
            'password': password,
            'admin': admin
        }
 
        self._append_record(data_dict=record)
 
        return record
 
    def _read_acl_file(self):
        """
            Read all the lines in `self.acl_file`
        """
        if not os.path.exists(self.acl_file):
            return None
 
        with open(self.acl_file, 'r') as f:
            lines = f.readlines()
 
        return lines
 
 
    def _unpack_data(self, buffer):
        """
            Unpack the buffer and extract contents.
        """
        unpacked_data = buffer.strip()
        unpacked_data = unpacked_data.split(':')
 
        record = {
            'username': unpacked_data[0],
            'password': unpacked_data[1],
            'admin': unpacked_data[2],
        }
        return record
 
 
    def verify(self, username, password):
        """
            Verify if username and password exist in ACL.
            - Client Facing
        """
        for line in self.acl_lines:
            try:
                data = self._unpack_data(line)
            except:
                continue
 
            if username == data['username'] and password == data['password']:
                return True, data
 
        return False
 
 
acl = ACL()
 
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', admin=False, flag=FLAG)
    elif request.method == 'POST':
        try:
            username = request.form.get('username')
            password = request.form.get('password')
            is_user, record = acl.verify(username, password)
            print(is_user)
            if is_user:
                admin = True if record['admin'] == 'true' else False
            else:
                raise Exception()
            return render_template('index.html', admin=admin, flag=FLAG, record=record)
        except:
            return redirect(url_for('index'))
 
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        acl.add_record(username, password, 'false')
 
        return redirect(url_for('index'))
 
if __name__ == '__main__':
    app.run(port=5000, debug=True)