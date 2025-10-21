#!/usr/bin/env node

/**
 * Simple Node.js test for Supabase connection
 * Run with: cd apps/frontend && node test-supabase.js
 */

const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = 'https://gyyiuhgcbggxzozasfji.supabase.co';
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imd5eWl1aGdjYmdneHpvemFzZmppIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTkwNTk5NjIsImV4cCI6MjA3NDYzNTk2Mn0.vumFtnaPhkZEosWAPlK01OHYWe-C_mAUhV_b6N0lMLE';

const supabase = createClient(supabaseUrl, supabaseKey);

async function testSupabaseConnection() {
    console.log('🔍 Testing Supabase Connection (Node.js)');
    console.log('='.repeat(50));
    console.log(`📍 URL: ${supabaseUrl}`);
    console.log(`🔑 Key: ${supabaseKey.substring(0, 20)}...`);

    try {
        // Test 1: Get session (should work without auth)
        console.log('\n1️⃣ Testing getSession...');
        const { data: sessionData, error: sessionError } = await supabase.auth.getSession();

        if (sessionError) {
            console.log(`❌ Session Error: ${sessionError.message}`);
        } else {
            console.log('✅ getSession successful');
            console.log(`   Session exists: ${!!sessionData.session}`);
        }

        // Test 2: Test signup with dummy data
        console.log('\n2️⃣ Testing signup...');
        const testEmail = `test-${Date.now()}@example.com`;
        const testPassword = 'testpassword123';

        const { data: signupData, error: signupError } = await supabase.auth.signUp({
            email: testEmail,
            password: testPassword
        });

        if (signupError) {
            console.log(`❌ Signup Error: ${signupError.message}`);
            console.log(`   Status: ${signupError.status}`);
        } else {
            console.log('✅ Signup successful!');
            console.log(`   User ID: ${signupData.user?.id}`);
            console.log(`   Email: ${signupData.user?.email}`);
            console.log(`   Email confirmed: ${!!signupData.user?.email_confirmed_at}`);
        }

        // Test 3: Test database connection (if tables exist)
        console.log('\n3️⃣ Testing database access...');
        try {
            const { data: dbData, error: dbError } = await supabase
                .from('profiles')
                .select('*')
                .limit(1);

            if (dbError) {
                console.log(`⚠️  Database access: ${dbError.message}`);
                console.log('   (This is normal if tables don\'t exist yet)');
            } else {
                console.log('✅ Database access successful');
                console.log(`   Found ${dbData?.length || 0} records`);
            }
        } catch (dbErr) {
            console.log(`⚠️  Database test failed: ${dbErr.message}`);
        }

    } catch (err) {
        console.log(`❌ Unexpected error: ${err.message}`);
    }

    console.log('\n' + '='.repeat(50));
    console.log('🎯 Node.js Connection Test Complete');
    console.log('\n💡 If signup works, CORS should work in browser too!');
    console.log('💡 If database access fails, tables might not be created yet.');
}

testSupabaseConnection();