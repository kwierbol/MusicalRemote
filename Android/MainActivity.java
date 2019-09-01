package com.example.karolinawierbol.multipilot;

import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.*;

import java.io.IOException;
import java.util.ArrayList;

public class MainActivity extends AppCompatActivity {

    //GUI elements
    private TextView title;
    private Button buttonNewQueue, buttonJoin;
    private SongsQueue songsQueue;

    public SongsQueue getSongsQueue() {
        return songsQueue;
    }
    private int whichPos;
    private String connectedDev;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        //GUI elements initialization
        title = (TextView) findViewById(R.id.textView); //rzutowanie, bo zwraca obiekt klasy View
        buttonNewQueue = (Button) findViewById(R.id.button);
        buttonJoin = (Button)findViewById(R.id.button2);

        AlertDialog.Builder builderSingle = new AlertDialog.Builder(this); // lista z polaczeniami bluetooth na telefonie

        builderSingle.setTitle("Select server:");


        final BluetoothConnection2 bc2 = new BluetoothConnection2();
        //check whether bluetooth is off
        if(bc2.isEnabled() == false){
            Utils.showToast(this, "NO BLUETOOTH CONNECTION!");
        }
        //when it's on, get paired devices list and connect to the chosen one
        else {
            ArrayList<String> pairedDevs = bc2.pairedDevices(); //sparowane urzadzenia wziete z fukncji

            final ArrayAdapter<String> arrayAdapter = new ArrayAdapter<String>(this, android.R.layout.simple_list_item_single_choice);
            for (int i = 0; i < pairedDevs.size(); i++) {
                arrayAdapter.add(pairedDevs.get(i));
            }

            builderSingle.setNegativeButton("ok", new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialog, int which) {
                    dialog.dismiss();
                    bc2.init(whichPos);
                    Utils.showToast(MainActivity.this, "CONNECT WITH " + connectedDev);
                }
            });

            builderSingle.setSingleChoiceItems(arrayAdapter,0, new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialog, int which) {
                    String devName = arrayAdapter.getItem(which);
                    connectedDev = devName;
                    whichPos = which;

                }

            });

            builderSingle.show(); //wyswietlanie listy sparowanych urzadzen do wybrania



        }


        //buttons actions
        buttonNewQueue.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(MainActivity.this, CreateNewQueueActivity.class));


            }
        });

        buttonJoin.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(MainActivity.this, AttachActivity.class));
            }
        });


    }

}
