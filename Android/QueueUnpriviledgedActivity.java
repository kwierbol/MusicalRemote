package com.example.karolinawierbol.multipilot;

import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.text.Editable;
import android.text.TextWatcher;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import java.io.IOException;

public class QueueUnpriviledgedActivity extends AppCompatActivity {

    //GUI elements
    TextView upperTitle, lowerTitle, songTitle, artistName;
    EditText prompt;
    Button buttonSend;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_queue_unpriviledged);

        //GUI elements initialization
        upperTitle = (TextView) findViewById(R.id.textView3);
        prompt = (EditText) findViewById(R.id.editText2);
        buttonSend = (Button) findViewById(R.id.button5);

        lowerTitle = (TextView) findViewById(R.id.textView4);
        songTitle = (TextView) findViewById(R.id.textView5);
        artistName = (TextView) findViewById(R.id.textView6);

        final SongsQueue sq = SongsQueue.getInstance();
        final BluetoothConnection2 bc2 = BluetoothConnection2.getInstance();

        songTitle.setText(sq.getCurrentSong().getTitle());
        artistName.setText(sq.getCurrentSong().getArtist());

        buttonSend.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String msg = "NEW_SONG" + prompt.getText().toString() + "\r\n";
                bc2.write(msg);
                String server_answer = null;
                try {
                    server_answer = bc2.receiveData();
                } catch (IOException e) {
                    Log.i("err_recv_msg", "Error while receiving message from server");
                }

                if (server_answer.equals("NEW_SONG_ERR\r\n")) {
                    Utils.showToast(QueueUnpriviledgedActivity.this, "BLAD PRZY DODAWANIU PIOSENKI!");
                }
            }
        });

    }
}