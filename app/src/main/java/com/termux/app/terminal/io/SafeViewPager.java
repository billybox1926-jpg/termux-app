package com.termux.app.terminal.io;

import android.content.Context;
import android.util.AttributeSet;
import android.view.MotionEvent;
import androidx.viewpager.widget.ViewPager;

/**
 * A safe wrapper around {@link ViewPager} that guards against IllegalArgumentException
 * caused by {@code MotionEvent} pointer index out of range errors on certain Android versions.
 *
 * <p>If {@link ViewPager#onInterceptTouchEvent(MotionEvent)} or
 * {@link ViewPager#onTouchEvent(MotionEvent)} throws an {@link IllegalArgumentException},
 * we catch it and return {@code false} to avoid the crash.
 * This mirrors the common workaround for the AndroidX bug (see issue #3478). </p>
 */
public class SafeViewPager extends ViewPager {
    public SafeViewPager(Context context) {
        super(context);
    }

    public SafeViewPager(Context context, AttributeSet attrs) {
        super(context, attrs);
    }

    @Override
    public boolean onInterceptTouchEvent(MotionEvent ev) {
        try {
            return super.onInterceptTouchEvent(ev);
        } catch (IllegalArgumentException e) {
            return ignoreBadPointerIndexTouchEvent();
        }
    }

    @Override
    public boolean onTouchEvent(MotionEvent ev) {
        try {
            return super.onTouchEvent(ev);
        } catch (IllegalArgumentException e) {
            return ignoreBadPointerIndexTouchEvent();
        }
    }

    /**
     * Pointer index out of range exceptions are caused by inconsistent multi-touch events
     * passed to ViewPager on some Android builds. Return false so the gesture is ignored
     * instead of crashing the app.
     */
    private boolean ignoreBadPointerIndexTouchEvent() {
        return false;
    }
}
