package com.example.karolinawierbol.multipilot;

import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.widget.TextView;

public class SettingsActivity extends AppCompatActivity {

    //GUI elements
    TextView parameter, IDnumber;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_settings);
        //GUI elements initialization
        parameter = (TextView) findViewById(R.id.textView9);
        IDnumber = (TextView) findViewById(R.id.textView10);
    }
}