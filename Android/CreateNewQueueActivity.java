package com.example.karolinawierbol.multipilot;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import java.io.IOException;

public class CreateNewQueueActivity extends AppCompatActivity {

    //GUI elements
    TextView message, ID;
    Button buttonEnter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_create_new_queue);

        //GUI elements initialization
        message = (TextView) findViewById(R.id.textView7);
        ID = (TextView) findViewById(R.id.textView8);
        buttonEnter = (Button) findViewById(R.id.button4);

        //present generated ID in the ID TextView field
        SongsQueue songsQueue = new SongsQueue();
        final int queueID = songsQueue.getID();
        ID.setText(Integer.toString(queueID));

        //buttons actions
        buttonEnter.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                BluetoothConnection2 bc2 = BluetoothConnection2.getInstance();
                String msg = "NEW_QUEUE" + Integer.toString(queueID) + "\r\n";
                bc2.write(msg);

                //get answer from server
                String server_answer = null;
                try {
                    server_answer = bc2.receiveData();
                } catch (IOException e) {
                    Log.i("err_recv_msg", "Error while receiving message from server");
                }

                //start new activity only if the server's answer allows you to do so
                if (server_answer.equals("NEW_QUEUE_ERROR\r\n")) {
                    Utils.showToast(CreateNewQueueActivity.this, "KOLEJKA JUZ ISTNIEJE");
                }
                else if (server_answer.equals("NEW_QUEUE_OK\r\n")) {
                    startActivity(new Intent(CreateNewQueueActivity.this, QueuePriviledgedActivity.class));
                }
                else {
                    Utils.showToast(CreateNewQueueActivity.this, "NIEPRAWIDLOWY KOMUNIKAT PROTOKOLU");
                }

            }
        });
    }
}
