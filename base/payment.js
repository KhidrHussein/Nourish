// Function to initiate the payment and redirect user
async function initiatePayment(amount, email) {
    try {
        const response = await fetch('/api/base/payments/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ amount: amount, email: email }),
        });
        const data = await response.json();
        if (response.ok) {
            window.location.href = data.payment_url; // Redirect to payment URL
        } else {
            console.error('Failed to initiate payment:', data.error);
        }
    } catch (error) {
        console.error('Error initiating payment:', error);
    }
}

// Function to handle webhook responses
async function handleWebhook(payload) {
    try {
        const response = await fetch('/api/base/paystack-webhook/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
        });
        const data = await response.json();
        if (response.ok) {
            console.log('Webhook response:', data);
            // Update UI based on payment status
        } else {
            console.error('Failed to handle webhook:', data.message);
        }
    } catch (error) {
        console.error('Error handling webhook:', error);
    }
}

// Example usage
initiatePayment(500, 'user@example.com'); // Initiate payment
handleWebhook({ event: 'charge.success', data: { /* webhook data */ } }); // Simulate webhook success
handleWebhook({ event: 'charge.failed', data: { /* webhook data */ } }); // Simulate webhook failure
