from .models import User,Expense , Transaction,Participant
from django.http import JsonResponse,Http404
from .tasks import send_expense_email


def create_user(request):

    if request.method == 'POST':
        userId = request.POST.get('userId')
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile_number = request.POST.get('mobile_number')

        user = User(userId= userId, name = name, email=email, mobile_number=mobile_number)
        user.save()
        return JsonResponse({'message':'User has been created'})
    else:
        return JsonResponse({'error':'Invalid request method'})

def create_expense(request):
    # Handle expense creation (POST request)
    # Validate data, split expenses, update user balances
    # Send asynchronous emails to participants
    if request.method == 'POST':
        description = request.POST.get('description')
        total_amount_str = request.POST.get('total_amount') 
        # participants_str = request.POST.get('participants')  # Comma-separated user IDs
        expense_type = request.POST.get('expense_type')

        participants_data = request.POST.getlist('participants')  # Assuming participants are submitted as a list of user IDs
        for participant_id in participants_data:
            user = User.objects.get(pk=participant_id)  # Assuming you have a User model
            participant_share = request.POST[f'share_{participant_id}']  # Assuming share is submitted as a form field
            Participant.objects.create(user=user, expense=expense, share=participant_share)

        # Check if total_amount is provided
        if total_amount_str is None:
            return JsonResponse({'error': 'Total amount is missing'})
        
        try:
            total_amount = float(total_amount_str)  # Convert to float
        except ValueError:
            return JsonResponse({'error': 'Invalid total amount'})

        # Parse participants' IDs

        try:
            participants = [int(user_id) for user_id in participants_str.split(',')]
        except ValueError:
            return JsonResponse({'error': 'Invalid user IDs provided'})

        # Save the expense to the database (assuming you have an Expense model)
        expense = Expense(description=description, total_amount=total_amount,
                          expense_type=expense_type)
        expense.save()
        expense.participants.set(participants)  # Set the participants

        subject = 'Expense Notification'
        message = 'You have been added to an expense. Total amount owed: INR -{total_amount}'
        recipient_list = ['participant1@example.com', 'participant2@example.com']
        send_expense_email.delay(subject, message, recipient_list)

        return JsonResponse({'message': 'Expense created successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'})

def get_user_expenses(request,user_id):
    try:
        if request.method == 'GET':
            user = User.objects.get(userId=user_id)  
    except User.DoesNotExist:
        raise Http404("Given user not found.")

    # Retrieve expenses for the specific user
    user_expenses = Expense.objects.filter(participants=user)

    formatted_expenses = []
    for expense in user_expenses:
        formatted_expenses.append({
            'expense_id': expense.id,
            'description': expense.description,
            'total_amount': expense.total_amount,
            'expense_type': expense.expense_type,
            # Add other relevant fields as needed
        })

    return JsonResponse({'user_expenses': formatted_expenses})

def get_balances(request):
    try:
        all_users = User.objects.all()  # Retrieve all users
    except User.DoesNotExist:
        raise Http404("No users found.")

    # Calculate balances for each user
    user_balances = {}
    for user in all_users:
        transactions = Transaction.objects.filter(user=user)
        balance = sum(transaction.amount for transaction in transactions)
        user_balances[user.id] = balance

    # Simplify balances
    # Example: Consolidate debts (negative balances)
    total_balance = sum(user_balances.values())
    avg_balance = total_balance / len(user_balances)
    for user_id, balance in user_balances.items():
        user_balances[user_id] -= avg_balance

    # Return balances as a JSON response
    return JsonResponse({'balances': user_balances})


def calculate_balances(expenses,simplify_expenses=False):
    """
    Calculate balances for users based on expenses.

    Args:
        expenses (list): List of dictionaries representing expenses.
            Each dictionary should have keys: 'participants', 'total_amount', and 'expense_type'.
            'participants' is a list of user IDs.
            'total_amount' is the total expense amount.
            'expense_type' can be 'EQUAL', 'EXACT', or 'PERCENT'.

    Returns:
        dict: A dictionary containing user balances (userId: balance).
    """
    balances = {}  # Dictionary to store balances (userId: balance)

    # Initialize balances
    for expense in expenses:
        for user_id in expense['participants']:
            balances.setdefault(user_id, 0)

    # Calculate balances based on expenses
    for expense in expenses:
        num_participants = len(expense['participants'])
        share_per_participant = 0

        if expense['expense_type'] == 'EQUAL':
            share_per_participant = expense['total_amount'] / num_participants
        elif expense['expense_type'] == 'EXACT':
            # Assuming you have predefined individual shares for this expense
            individual_shares = [100, 200, 150]  # Example: Adjust as needed
            if len(individual_shares) == num_participants:
                share_per_participant = sum(individual_shares) / num_participants
        elif expense['expense_type'] == 'PERCENT':
            # Assuming you have predefined percentages for this expense
            percentages = [30, 40, 30]  # Example: Adjust as needed
            if sum(percentages) == 100:
                share_per_participant = (expense['total_amount'] * percentages[user_id]) / 100

        # Update balances for participants
        for user_id in expense['participants']:
            balances[user_id] += share_per_participant

    # Simplify expenses if requested
    if simplify_expenses:
        total_balance = sum(balances.values())
        avg_balance = total_balance / len(balances)
        for user_id in balances:
            balances[user_id] -= avg_balance

    return balances

# Example usage
expenses_data = [
    {
        'participants': [1, 2, 3],
        'total_amount': 300,
        'expense_type': 'EQUAL',
    },
    # Add more expenses here...
]

user_balances = calculate_balances(expenses_data)
print(user_balances)  # Example output: {1: 100.0, 2: 100.0, 3: 100.0}
