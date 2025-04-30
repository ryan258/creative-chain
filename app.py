from flask import Flask, render_template, request, redirect, url_for, session
import sys
import json
sys.path.append('.')  # Ensure project root is in path
from crew.idea_jam import InteractiveIdeaJamToPrototypeCrew
from crew.prototype import GPTPrototypeCrew
from crew.critic import InteractivePrototypeToCriticCrew
from crew.reiterate import GPTReiterateCrew

app = Flask(__name__)
app.secret_key = 'replace-this-with-a-secret-key'  # Needed for session

# Home page
@app.route('/')
def home():
    return render_template('home.html')

# Main workflow page (start flow)
@app.route('/workflow', methods=['GET', 'POST'])
def workflow():
    return render_template('workflow.html')

@app.route('/start_flow', methods=['POST'])
def start_flow():
    topic = request.form['topic']
    num_ideas = int(request.form.get('num_ideas', 9))
    session['topic'] = topic
    session['num_ideas'] = num_ideas
    session['step'] = 'variation_factors'
    # Show the variation factors form (sliders)
    return render_template('variation_factors.html')

@app.route('/variation_factors', methods=['POST'])
def variation_factors():
    print('\n[DEBUG] Incoming POST data:', dict(request.form))
    print('[DEBUG] Session:', dict(session))
    # Get slider values or randomize if not present
    tech = int(request.form.get('technology', 5))
    biz = int(request.form.get('business', 5))
    fantasy = int(request.form.get('fantasy', 5))
    session['variation_factors'] = {'technology': tech, 'business': biz, 'fantasy': fantasy}
    # Compose variation string for prompt
    variation_str = f"technology:{tech}, business:{biz}, fantasy:{fantasy}"
    topic = session['topic']
    num_ideas = session.get('num_ideas', 5)
    # Ensure num_ideas is used in the prompt
    prompt = f"{topic} | variation={variation_str} | num_ideas={num_ideas}"
    crew = InteractiveIdeaJamToPrototypeCrew()
    result = crew.run_web(prompt)
    ideas = result.get('ideas', [])
    clusters = result.get('clusters', [])
    # Flatten ideas for UI
    flat_ideas = []
    idea_counter = 0
    for idea in ideas:
        flat_ideas.append({
            'text': idea.get('text', str(idea)),
            'idx': idea_counter,
            'cluster': idea.get('cluster', '')
        })
        idea_counter += 1
    # Limit to num_ideas
    flat_ideas = flat_ideas[:num_ideas]
    session['ideas'] = flat_ideas
    print(f"[DEBUG] flat_ideas length: {len(flat_ideas)}")
    if not flat_ideas:
        error_msg = result.get('error') or '[No ideas generated. Try again or check your prompt.]'
        return render_template('idea_clusters_inner.html', ideas=[], error=error_msg)
    return render_template('idea_clusters_inner.html', ideas=flat_ideas, error=None)

@app.route('/pick_idea', methods=['POST'])
def pick_idea():
    try:
        chosen_idx = int(request.form['choice'])
        ideas = session.get('ideas', [])
        if not ideas or chosen_idx < 0 or chosen_idx >= len(ideas):
            return render_template('flow_step.html', step_title='Error', output='Invalid idea selection. Please return and pick a valid idea.', next_action=url_for('start_flow'), show_choices=False)
        chosen_idea = ideas[chosen_idx]['text']
        session['chosen_idea'] = chosen_idea
        session['step'] = 'prototype'
        # Use real Prototype logic
        proto_agent = GPTPrototypeCrew()
        prototype = proto_agent.run(chosen_idea)
        session['prototype'] = prototype
        return render_template('flow_step.html', step_title='Prototype 🛠', output=prototype, next_action=url_for('run_critic'), show_choices=False)
    except Exception as e:
        return render_template('flow_step.html', step_title='Error', output=f'Error picking idea: {e}', next_action=url_for('start_flow'), show_choices=False)

@app.route('/run_critic', methods=['POST'])
def run_critic():
    idea = session.get('chosen_idea', '')
    prototype = session.get('prototype', '')
    # Use real Critic logic
    critic_agent = InteractivePrototypeToCriticCrew()
    critique = critic_agent.run((idea, prototype))
    session['critique'] = critique
    session['step'] = 'critic'
    return render_template('flow_step.html', step_title='Critic 🔍', output=critique.replace('\n', '<br>'), next_action=url_for('run_reiterate'), show_choices=False)

@app.route('/run_reiterate', methods=['POST'])
def run_reiterate():
    prototype = session.get('prototype', '')
    critique = session.get('critique', '')
    # Use real Reiterate logic
    reiterate_agent = GPTReiterateCrew()
    improved = reiterate_agent.run((prototype, critique))
    session['improved'] = improved
    session['step'] = 'reiterate'
    return render_template('flow_step.html', step_title='Reiterate 🔄', output=improved, next_action=url_for('save_to_vault'), show_choices=False)

@app.route('/save_to_vault', methods=['POST'])
def save_to_vault():
    improved = session.get('improved', '')
    idea = session.get('chosen_idea', '')
    prototype = session.get('prototype', '')
    critique = session.get('critique', '')
    # Save to markdown in ideas/ (like CLI)
    import os, datetime
    os.makedirs('ideas', exist_ok=True)
    safe_title = re.sub(r'[^a-zA-Z0-9_\-]', '_', idea[:40])
    filename = f'ideas/{safe_title}_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f'# {idea}\n\n## Prototype\n{prototype}\n\n## Critique\n{critique}\n\n## Improved Version\n{improved}\n')
    session['step'] = 'vault'
    vault_msg = f"Saved to vault as <code>{filename}</code>!"
    return render_template('flow_step.html', step_title='Vault 🏛', output=vault_msg, next_action=url_for('home'), show_choices=False)

if __name__ == '__main__':
    app.run(debug=True)
