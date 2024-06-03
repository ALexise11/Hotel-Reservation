// Replace 'your_public_key' with your actual Stripe public key
var stripe = Stripe('your_public_key');
var elements = stripe.elements();

// Create an instance of the card Element.
var card = elements.create('card');

// Add an instance of the card Element into the `card-element` div.
card.mount('#card-element');

// Handle real-time validation errors from the card Element.
card.addEventListener('change', function(event) {
  var displayError = document.getElementById('card-errors');
  if (event.error) {
    displayError.textContent = event.error.message;
  } else {
    displayError.textContent = '';
  }
});

// Handle form submission.
var form = document.getElementById('payment-form');
form.addEventListener('submit', function(event) {
  event.preventDefault();

  // Disable the submit button to prevent repeated clicks.
  document.querySelector('button[type="submit"]').disabled = true;

  // Create payment method and confirm payment intent
  stripe.createPaymentMethod({
    type: 'card',
    card: card,
    billing_details: {
      name: document.getElementById('card-holder-name').value
    }
  }).then(function(result) {
    if (result.error) {
      // Inform the user if there was an error.
      var errorElement = document.getElementById('card-errors');
      errorElement.textContent = result.error.message;

      // Enable the submit button.
      document.querySelector('button[type="submit"]').disabled = false;
    } else {
      // Insert the payment method ID into the form so it gets submitted to the server.
      var form = document.getElementById('payment-form');
      var hiddenInput = document.createElement('input');
      hiddenInput.setAttribute('type', 'hidden');
      hiddenInput.setAttribute('name', 'payment_method_id');
      hiddenInput.setAttribute('value', result.paymentMethod.id);
      form.appendChild(hiddenInput);

      // Submit the form.
      form.submit();
    }
  });
});
