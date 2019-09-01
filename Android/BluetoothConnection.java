package com.example.karolinawierbol.multipilot;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;
import android.os.ParcelUuid;
import android.util.Log;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.UnsupportedEncodingException;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.Set;


public class BluetoothConnection extends MainActivity{

    private static BluetoothConnection instance;

    private OutputStream outputStream = null;
    private InputStream inStream = null;
    private BluetoothSocket sock = null;

    public static BluetoothConnection getInstance() {
        return instance;
    }

    public void init(int whichPos)  {

        instance = this;

        BluetoothAdapter bluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
        if (bluetoothAdapter != null) {
            if (bluetoothAdapter.isEnabled()) {
                Set<BluetoothDevice> bondedDevices = bluetoothAdapter.getBondedDevices();
                if(bondedDevices.size() > 0) {
                    Object[] devices = (Object []) bondedDevices.toArray();
                    BluetoothDevice device = (BluetoothDevice) devices[whichPos]; //position in array dependent on phone's internal life

                    Log.d("myDevice",device.getAddress()); //should log address of the server
                    Log.d("myDevice",device.getName());

                    ParcelUuid[] uuids = device.getUuids(); //gets UUIDs of all devices

                    Log.d("myUuid",uuids[whichPos].toString()); //the position MUST match the position from devices variable


//                    BluetoothSocket sock = null;
                    Method m = null;
                    try {
                        m = device.getClass().getMethod("createRfcommSocket", new Class[]{int.class});
                        sock = (BluetoothSocket) m.invoke(device,3);
                        sock.connect();
                        Log.d("myMsg","Connected: "+sock.getRemoteDevice().getName());
                        outputStream = sock.getOutputStream();
                        inStream = sock.getInputStream();

                    } catch (NoSuchMethodException e) {
                        e.printStackTrace();
                        Log.d("myMsg","no method: " + e.getMessage());

                    } catch (IllegalAccessException e) {
                        e.printStackTrace();
                        Log.d("myMsg","illegal access: " + e.getMessage());

                    } catch (InvocationTargetException e) {
                        e.printStackTrace();
                        Log.d("myMsg","invocation target: " + e.getMessage());
                    } catch (IOException e) {
                        Log.d("myMsg", "failed conn: " + e.getMessage());
                        e.printStackTrace();
                    }

                }


            } else {
                Log.e("myTag", "NO CONNECTION");
            }
        }
    }

    public ArrayList<String> pairedDevices() {

        BluetoothAdapter bluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
        ArrayList<String> pairedDevs = new ArrayList<>(); //necessary to show paired devices

        if (bluetoothAdapter != null && bluetoothAdapter.isEnabled()) {
            Set<BluetoothDevice> bondedDevices = bluetoothAdapter.getBondedDevices();
            for (BluetoothDevice bt : bondedDevices) { //potrzebne do wsywietlenie sparowanych urzadzen
                pairedDevs.add(bt.getName() + "\n" + bt.getAddress());
            }
        }
        return pairedDevs;
    }

    public boolean isEnabled() {
        BluetoothAdapter bluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
        if (bluetoothAdapter != null && bluetoothAdapter.isEnabled())
            return true;
        return false;
    }

    public void write(String s)  {
        try {
            outputStream.write(s.getBytes());
        } catch (IOException e)
        {
            Log.d("myMsg","error: "+ e.getMessage());
        }
    }

    public String decodeString(String encodedString) {
        try {
            return new String(encodedString.getBytes(), "UTF-8");
        } catch (UnsupportedEncodingException e) {
            Log.e("unsupCODING", "Unsupported coding exception");
        }
        return "";
    }

    public String receiveData() throws IOException{
        byte[] buffer = new byte[1];
        int bytes;

        String delimiter = "\r\n";
        String deliveredMessage = "";

        while (true) {
            try {
                InputStream is = this.inStream;
                while (!deliveredMessage.endsWith(delimiter)) {
                    bytes = is.read(buffer);

                    String lastChar = new String(buffer, 0, bytes);
                    lastChar = this.decodeString(lastChar);
                    deliveredMessage += lastChar;
                }
            } catch (IOException e) {
                Log.e("my_bluetooth_err", "Blad przy czytaniu danych");
                e.printStackTrace();
                return null;
            }
            return deliveredMessage;
        }
    }

    public InputStream getInStream(){
        return this.inStream;
    }

    public OutputStream getOutputStream(){
        return this.outputStream;
    }

    public void run() {

        int BUFF = 1024;
        byte[] buffer = new byte[BUFF];
        int bytes = 0;
        int b = BUFF;

        while (true) {
            try {
                bytes = inStream.read(buffer, bytes, BUFF - bytes);
            } catch (IOException e) {
                e.printStackTrace();
                Log.d("myMsg","eror: "+e.getMessage());
            }
        }
    }

    public void close(){
        try {
            this.sock.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

}
