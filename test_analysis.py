import requests
import json

print('🔄 Testing GitHub Issue Analysis...')
print('='*60)

payload = {
    'repo_url': 'https://github.com/facebook/react',
    'issue_number': 1
}

print('📝 Request:')
print('   Repository: https://github.com/facebook/react')
print('   Issue: #1')
print()
print('⏳ Sending request to backend...')
print()

try:
    response = requests.post('http://localhost:8000/analyze', json=payload, timeout=60)
    
    if response.status_code == 200:
        result = response.json()
        print('✅ SUCCESS! Analysis Result:')
        print('='*60)
        print(json.dumps(result, indent=2))
        print('='*60)
        print()
        print('🔍 Validation:')
        summary = result.get('summary', 'MISSING')[:50]
        issue_type = result.get('type', 'MISSING')
        priority = result.get('priority_score', 'MISSING')[:30]
        labels = result.get('suggested_labels', [])
        impact = result.get('potential_impact', 'MISSING')[:50]
        
        print(f'   ✓ Summary: {summary}...')
        print(f'   ✓ Type: {issue_type}')
        print(f'   ✓ Priority: {priority}...')
        print(f'   ✓ Labels: {labels}')
        print(f'   ✓ Impact: {impact}...')
    else:
        print(f'❌ Error: Status {response.status_code}')
        print(response.text)
except requests.exceptions.Timeout:
    print('⏳ Request is taking longer (might be processing). Check backend logs.')
except Exception as e:
    print(f'❌ Error: {e}')
