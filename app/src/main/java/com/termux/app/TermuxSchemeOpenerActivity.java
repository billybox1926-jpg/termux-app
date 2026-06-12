package com.termux.app;

import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;

/**
 * Trampoline activity that handles {@code termux:} URI schemes by forwarding
 * to {@link TermuxOpenReceiver} which runs the scheme-opener script. The activity
 * is immediately finished after forwarding the intent. (#3945)
 */
public class TermuxSchemeOpenerActivity extends android.app.Activity {

    private static final String LOG_TAG = "TermuxSchemeOpener";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        Intent intent = getIntent();
        Uri data = intent.getData();
        if (data == null) {
            android.util.Log.e(LOG_TAG, "Called without intent data");
            finish();
            return;
        }

        android.util.Log.d(LOG_TAG, "termux: URI received: " + data);

        Intent receiverIntent = new Intent(this, TermuxOpenReceiver.class);
        receiverIntent.setData(data);
        receiverIntent.setAction(intent.getAction());
        if (intent.getExtras() != null) {
            receiverIntent.putExtras(intent.getExtras());
        }
        sendBroadcast(receiverIntent);

        finish();
    }
}
