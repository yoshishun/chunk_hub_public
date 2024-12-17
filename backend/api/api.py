from . import *

@api.route("/ranking", methods=["GET"])
@login_required
def get_users_ranking():
    sql = """
    SELECT u.name, SUM(IFNULL(cs.pronounced_count, 0)) as total_pronounced_count
    FROM tbl_users 
    LEFT JOIN tbl_chunk_sentences cs ON u.id = cs.user_id
    GROUP BY u.id
    ORDER BY total_pronounced_count DESC
    """
    result = db_mng.fetch_query(sql)
    return jsonify(result)

@api.route("/account/profile", methods=["GET"])
@login_required
def get_profile():
    user_id = session['user_id']
    user_data = db_mng.fetch_query("SELECT id, name, email FROM tbl_users WHERE id = %s", (user_id,))
    if user_data:
        return jsonify(user_data[0])
    else:
        return jsonify({"error": "User not found"}), 404

@api.route("/folders/name", methods=["GET"])
@login_required
def get_folder_name():
    folder_id = request.args.get('fid')
    user_id = session['user_id']
    result = Folder.get_folder_name(db_mng, folder_id, user_id)
    if result:
        return jsonify({"name": result[0]['name']})
    else:
        return jsonify({"error": "Folder not found"}), 404

@api.route("/chunk_folders/list", methods=["GET"])
@login_required
def get_chunk_folders_list():
    user_id = session['user_id']
    folder_class = request.args.get('fclass')
    all_folder_rows = Folder.get_chunk_folders_list(db_mng, user_id, folder_class)
    result_json = []
    for folder_row in all_folder_rows:
        create_date = folder_row['create_date'].strftime('%Y-%m-%d') if folder_row['create_date'] else None
        update_date = folder_row['update_date'].strftime('%Y-%m-%d') if folder_row['update_date'] else None
        item = {
            "id": folder_row['id'],
            "user_id": folder_row['user_id'],
            "class": folder_row['class'],
            "name": folder_row['name'],
            "notes": folder_row['notes'],
            "create_date": create_date,
            "update_date": update_date,
        }
        result_json.append(item)
    return jsonify(result_json)

@api.route("/folders/list")
@login_required
def get_folders_list_all():
    user_id = session['user_id']
    all_folder_rows = Folder.get_folders_list_all(db_mng, user_id)
    result_json = []
    for folder_row in all_folder_rows:
        create_date = folder_row['create_date'].strftime('%Y-%m-%d') if folder_row['create_date'] else None
        update_date = folder_row['update_date'].strftime('%Y-%m-%d') if folder_row['update_date'] else None
        item = {
            "id": folder_row['id'],
            "user_id": folder_row['user_id'],
            "class": folder_row['class'],
            "name": folder_row['name'],
            "notes": folder_row['notes'],
            "create_date": create_date,
            "update_date": update_date,
        }
        result_json.append(item)
    return jsonify(result_json)

@api.route("/folders/list/add", methods=["POST"])
@login_required
def add_folders():
    folder_id = "fid_" + ''.join(random.choice(string.ascii_letters) for _ in range(10))
    folder_user_id = session['user_id']
    folder_class = request.json['class']
    folder_name = request.json['name']
    folder_notes = request.json['notes']
    now = datetime.now()
    folder_create_date = now.strftime('%Y-%m-%d %H:%M:%S')
    Folder.add_folder(db_mng, folder_id, folder_user_id, folder_class, folder_name, folder_notes, folder_create_date)
    return jsonify({'success': True})

@api.route("/folders/edit", methods=["PUT"])
@login_required
def edit_folder():
    data = request.json
    folder_id = data.get('id')
    name = data.get('name')
    notes = data.get('notes')
    user_id = session['user_id']
    update_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    Folder.edit_folder(db_mng, folder_id, user_id, name, notes, update_date)
    return jsonify({'success': True})

@api.route("/folders/delete", methods=["DELETE"])
@login_required
def delete_folder():
    data = request.json
    folder_id = data.get('id')
    user_id = session['user_id']
    
    
    chunks = Chunk.get_all_chunks_list(db_mng, user_id, folder_id)
    for chunk in chunks:
        Chunk.delete_chunk(db_mng, user_id, chunk['id'])
        links = ChunkSentenceLink.get_links(db_mng, user_id, chunk['id'])
        for link in links:
            ChunkSentenceLink.delete_links(db_mng, link['chunk_id'])

    chunk_sentences = ChunkSentence.get_chunk_sentences_list(db_mng, user_id, folder_id)
    for chunk_sentence in chunk_sentences:
        ChunkSentence.delete_chunk_sentence(db_mng, user_id, chunk_sentence['id'])
        links = ChunkSentenceLink.get_links(db_mng, user_id, chunk_sentence['id'])
        for link in links:
            ChunkSentenceLink.delete_links(db_mng, link['chunk_id'])
    
    Folder.delete_folder(db_mng, folder_id, user_id)
    
    return jsonify({"message": "Folder and related data deleted successfully"})



@api.route("/folders/total_pronounced_count", methods=["GET"])
@login_required
def get_total_pronounced_count():
    folder_id = request.args.get('fid')
    user_id = session['user_id']
    if folder_id:
        total_count = Folder.get_total_pronounced_count(db_mng, folder_id, user_id)
        return jsonify({"total_pronounced_count": total_count})
    else:
        return jsonify({"error": "Folder ID is required"}), 400


@api.route("/folders/item_count", methods=["GET"])
@login_required
def get_item_count():
    folder_id = request.args.get('fid')
    user_id = session['user_id']
    if folder_id:
        item_count = Folder.get_item_count(db_mng, folder_id, user_id)
        return jsonify({"item_count": item_count})
    else:
        return jsonify({"error": "Folder ID is required"}), 400


@api.route("/chunks/list")
@login_required
def get_all_chunks_list():
    folder_id = request.args.get('fid')
    user_id = session['user_id']
    all_chunk_rows = Chunk.get_all_chunks_list(db_mng, user_id, folder_id)
    result_json = []
    for chunk_row in all_chunk_rows:
        item = {
            "id": chunk_row['id'],
            "user_id": chunk_row['user_id'],
            "folder_id": chunk_row['folder_id'],
            "learning_chunk": chunk_row['learning_chunk'],
            "translating_chunk": chunk_row['translating_chunk'],
            "pronounced_count": chunk_row['pronounced_count'],
            "politeness": chunk_row['politeness'],
            "nuance": chunk_row['nuance'],  
            "situation": chunk_row['situation'],  
            "notes": chunk_row['notes'],
            "create_date": chunk_row['create_date'],
            "update_date": chunk_row['update_date']
        }
        result_json.append(item)
        
    return jsonify(result_json)

@api.route("/chunks/move", methods=["POST"])
@login_required
def move_chunk():
    data = request.json
    chunk_ids = data.get('chunk_ids')
    target_folder_id = data.get('target_folder_id')
    user_id = session['user_id']

    if not chunk_ids or not target_folder_id:
        return jsonify({'error': 'Invalid data'}), 400

    try:
        for chunk_id in chunk_ids:
            sql = 'UPDATE tbl_chunks SET folder_id = %s WHERE id = %s AND user_id = %s'
            params = (target_folder_id, chunk_id, user_id)
            db_mng.execute_query(sql, params)

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route("/chunk_sentences/move", methods=["POST"])
@login_required
def move_chunk_sentence():
    data = request.json
    chunk_sentence_ids = data.get('chunk_sentence_ids')
    target_folder_id = data.get('target_folder_id')
    user_id = session['user_id']

    if not chunk_sentence_ids or not target_folder_id:
        return jsonify({'error': 'Invalid data'}), 400

    try:
        for chunk_sentence_id in chunk_sentence_ids:
            sql = 'UPDATE tbl_chunk_sentences SET folder_id = %s WHERE id = %s AND user_id = %s'
            params = (target_folder_id, chunk_sentence_id, user_id)
            db_mng.execute_query(sql, params)

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route("/chunks/list/add", methods=["POST"])
@login_required
def add_chunks():
    user_id = session['user_id']
    folder_id = request.args.get('fid')
    now = datetime.now()
    chunk_create_date = now.strftime('%Y-%m-%d %H:%M:%S')
    data = request.json
    formDataList = data.get('form_data_list', [])
    for formData in formDataList:
        chunk_id = "cid_" + ''.join(random.choice(string.ascii_letters) for _ in range(10))
        learning_chunk = formData.get('learning_chunk', '')
        translating_chunk = formData.get('translating_chunk', '')
        politeness = formData.get('politeness', 0)
        nuance = formData.get('nuance', '')
        situation = formData.get('situation', '')
        notes = formData.get('notes', '')
        Chunk.add_chunk(db_mng, chunk_id, user_id, folder_id, learning_chunk, translating_chunk, politeness, nuance, situation, notes, chunk_create_date)
                
    return jsonify({'success': True})

@api.route("/chunks/list/edit", methods=["POST"])
@login_required
def chunks_edit():
    user_id = session['user_id']
    now = datetime.now()
    chunk_update_date = now.strftime('%Y-%m-%d %H:%M:%S')
    data = request.json
    deleteDataList = data.get('deleteDataList', [])
    editDataList = data.get('editDataList', [])
    
    
    if deleteDataList:
        for formData in deleteDataList:
            chunk_id = formData.get('id', '')
            if chunk_id:
                Chunk.delete_chunk(db_mng, user_id, chunk_id)
    
    
    if editDataList:
        for formData in editDataList:
            chunk_id = formData.get('id', '')
            learning_chunk = formData.get('learning_chunk', '')
            translating_chunk = formData.get('translating_chunk', '')
            politeness = formData.get('politeness', 0)
            nuance = formData.get('nuance', '')
            situation = formData.get('situation', '')
            notes = formData.get('notes', '')
            Chunk.edit_chunk(db_mng, learning_chunk, translating_chunk, politeness, nuance, situation, notes, chunk_update_date, user_id, chunk_id)
            
    return jsonify({'success': True})

@api.route("/chunk_sentences/list")
@login_required
def get_chunk_sentences_list():
    folder_id = request.args.get('fid')
    user_id = session['user_id']
    all_chunk_sentence_rows = ChunkSentence.get_chunk_sentences_list(db_mng, user_id, folder_id)
    folder_dict = {}
    
    for chunk_sentence_row in all_chunk_sentence_rows:
        folder_id = chunk_sentence_row['folder_id']
        
        if folder_id not in folder_dict:
            folder_dict[folder_id] = {
                "folder_id": folder_id,
                "folder_name": Folder.get_folder_name(db_mng, folder_id, user_id)[0]['name'],
                "chunk_sentences": []
            }
            
        sql = 'SELECT * FROM tbl_chunks c ' \
              'LEFT JOIN tbl_chunk_sentence_links l ' \
              'ON c.id = l.chunk_id ' \
              'WHERE c.user_id=%s AND l.sentence_id=%s'
        params = (user_id, chunk_sentence_row['id'])
        used_chunk_rows = db_mng.fetch_query(sql, params)
        used_chunk_list = []
        for used_chunk in used_chunk_rows:
            used_chunk_list.append({
                "title": used_chunk['learning_chunk'],
                "value": {
                    "user_id": used_chunk['user_id'],
                    "folder_id": used_chunk['folder_id'],
                    "chunk_id": used_chunk['id'],
                    "learning_chunk": used_chunk['learning_chunk'],
                    "translating_chunk": used_chunk['translating_chunk'],
                    "pronounced_count": used_chunk['pronounced_count'],
                    "politeness": used_chunk['politeness'],
                    "nuance": used_chunk['nuance'],  
                    "situation": used_chunk['situation'],  
                    "notes": used_chunk['notes'],
                    "create_date": used_chunk['create_date'],
                    "update_date": used_chunk['update_date']
                }
            })
        item = {
            "id": chunk_sentence_row['id'],
            "user_id": chunk_sentence_row['user_id'],
            "folder_id": chunk_sentence_row['folder_id'],
            "chunk_sentence": chunk_sentence_row['chunk_sentence'],
            "translating_sentence": chunk_sentence_row['translating_sentence'],
            "used_chunks": used_chunk_list,
            "pronounced_count": chunk_sentence_row['pronounced_count'],
            "politeness": chunk_sentence_row['politeness'],
            "situation": chunk_sentence_row['situation'],
            "notes": chunk_sentence_row['notes'],
            "create_date": chunk_sentence_row['create_date'],
            "update_date": chunk_sentence_row['update_date'],
        }
        folder_dict[folder_id]['chunk_sentences'].append(item)
    
    result_json = list(folder_dict.values())
    return jsonify(result_json)

@api.route("/chunk_sentences/list/create", methods=["POST"])
@login_required
def create_chunk_sentences():
    user_id = session['user_id']
    folder_id = request.args.get('fid')
    now = datetime.now()
    chunk_sentence_create_date = now.strftime('%Y-%m-%d %H:%M:%S')
    data = request.json
    formDataList = data.get('form_data_list', [])
    newChunks = data.get('new_chunks', [])
    if newChunks:
        for chunk in newChunks:
            chunk_id = "cid_" + ''.join(random.choice(string.ascii_letters) for _ in range(10))
            save_folder_id = chunk['value']['folder_id']
            learning_chunk = chunk['value']['learning_chunk']
            translating_chunk = chunk['value']['translating_chunk']
            politeness = chunk['value'].get('politeness', 0) 
            nuance = chunk['value'].get('nuance', '')  
            situation = chunk['value'].get('situation', '')  
            notes = chunk['value'].get('notes', '')  
            Chunk.add_chunk(db_mng, chunk_id, user_id, save_folder_id, learning_chunk, translating_chunk, politeness, nuance, situation, notes, chunk_sentence_create_date)
                
    for formData in formDataList:
        chunk_sentence_id = "csid_" + ''.join(random.choice(string.ascii_letters) for _ in range(10))
        chunk_sentence = formData.get('chunk_sentence', '')
        translating_sentence = formData.get('translating_sentence', '')
        selected_used_chunks = formData.get('used_chunks', [])
        politeness = formData.get('politeness', 0) 
        situation = formData.get('situation', '')
        notes = formData.get('notes', '')
        ChunkSentence.create_chunk_sentence(db_mng, chunk_sentence_id, user_id, folder_id, chunk_sentence, translating_sentence, politeness, situation, notes, chunk_sentence_create_date)
        
        for selected_used_chunk in selected_used_chunks:
            chunk_id = selected_used_chunk['value']['chunk_id']
            if chunk_id:
                ChunkSentenceLink.add_link(db_mng, user_id, chunk_id, chunk_sentence_id, chunk_sentence_create_date)
            else:
                sql = 'SELECT id FROM tbl_chunks WHERE learning_chunk=%s AND user_id=%s'
                params = (selected_used_chunk['title'], user_id)
                new_chunk_id = db_mng.fetch_query(sql, params)
                if new_chunk_id:
                    ChunkSentenceLink.add_link(db_mng, user_id, new_chunk_id[0]['id'], chunk_sentence_id, chunk_sentence_create_date)
    return jsonify({'success': True})

@api.route("/chunk_sentences/list/edit", methods=["POST"])
@login_required
def chunk_sentences_edit():
    user_id = session['user_id']
    now = datetime.now()
    create_date = now.strftime('%Y-%m-%d %H:%M:%S')
    update_date = now.strftime('%Y-%m-%d %H:%M:%S')
    data = request.json
    deleteDataList = data.get('deleteDataList', [])
    editDataList = data.get('editDataList', [])
    newChunks = data.get('newChunks', [])
    if newChunks:
        for chunk in newChunks:
            chunk_id = "cid_" + ''.join(random.choice(string.ascii_letters) for _ in range(10))
            folder_id = chunk['value']['folder_id']
            learning_chunk = chunk['value']['learning_chunk']
            translating_chunk = chunk['value']['translating_chunk']
            politeness = chunk['value'].get('politeness', 0) 
            nuance = chunk['value'].get('nuance', '')  
            situation = chunk['value'].get('situation', '')  
            notes = chunk['value'].get('notes', '')  
            Chunk.add_chunk(db_mng, chunk_id, user_id, folder_id, learning_chunk, translating_chunk, politeness, nuance, situation, notes, create_date)
            
    if deleteDataList:
        for formData in deleteDataList:
            chunk_sentence_id = formData.get('id', '')
            ChunkSentence.delete_chunk_sentence(db_mng, user_id, chunk_sentence_id)
            ChunkSentenceLink.delete_links(db_mng, chunk_sentence_id)
    if editDataList:
        for formData in editDataList:
            chunk_sentence_id = formData.get('id', '')
            chunk_sentence = formData.get('chunk_sentence', '')
            translating_sentence = formData.get('translating_sentence', '')
            politeness = formData.get('politeness', 0) 
            situation = formData.get('situation', '')
            notes = formData.get('notes', '')
            ChunkSentence.edit_chunk_sentence(db_mng, chunk_sentence, translating_sentence, politeness, situation, notes, update_date, user_id, chunk_sentence_id)
            ChunkSentenceLink.delete_links(db_mng, chunk_sentence_id)
            selected_used_chunks = formData.get('used_chunks', [])
            for selected_used_chunk in selected_used_chunks:
                chunk_id = selected_used_chunk['value']['chunk_id']
                if chunk_id:
                    ChunkSentenceLink.add_link(db_mng, user_id, chunk_id, chunk_sentence_id, create_date)
                else:
                    sql = 'SELECT id FROM tbl_chunks WHERE learning_chunk=%s AND user_id=%s'
                    params = (selected_used_chunk['title'], user_id)
                    new_chunk_id = db_mng.fetch_query(sql, params)
                    if new_chunk_id:
                        ChunkSentenceLink.add_link(db_mng, user_id, new_chunk_id[0]['id'], chunk_sentence_id, create_date)
    return jsonify({'success': True})

@api.route("/chunk_sentences/list/update_pronounced_count", methods=["POST"])
@login_required
def update_pronounced_count():
    user_id = session['user_id']
    now = datetime.now()
    update_date = now.strftime('%Y-%m-%d %H:%M:%S')
    data = request.json
    editDataList = data.get('editDataList', [])

    if editDataList:
        for formData in editDataList:
            chunk_sentence_id = formData.get('id', '')
            pronounced_count = formData.get('pronounced_count', 0)
            current_session_count = formData.get('current_session_count', 0)

            
            ChunkSentence.update_pronounced_count(db_mng, pronounced_count, update_date, user_id, chunk_sentence_id)

            
            ChunkSentencePronouncedCount.add_or_update_pronounced_count(db_mng, user_id, chunk_sentence_id, current_session_count, update_date)

            
            sql = 'SELECT chunk_id FROM tbl_chunk_sentence_links WHERE sentence_id=%s'
            params = (chunk_sentence_id,)
            used_chunk_rows = db_mng.fetch_query(sql, params)
            for used_chunk in used_chunk_rows:
                chunk_id = used_chunk['chunk_id']
                sql = 'SELECT pronounced_count FROM tbl_chunks WHERE id=%s'
                params = (chunk_id,)
                chunk_rows = db_mng.fetch_query(sql, params)
                for chunk_row in chunk_rows:
                    chunk_pronounced_count = chunk_row['pronounced_count']
                    chunk_pronounced_count += current_session_count
                    Chunk.update_pronounced_count(db_mng, chunk_pronounced_count, update_date, user_id, chunk_id)

                    
                    ChunkPronouncedCount.add_or_update_pronounced_count(db_mng, user_id, chunk_id, current_session_count, update_date)

    return jsonify({'success': True})


@api.route("/test/pyvis", methods=["GET", "POST"])
@login_required
def pyvis_test():
    user_id = session['user_id']
    sql_chunks = 'SELECT id, learning_chunk, pronounced_count FROM tbl_chunks WHERE user_id=%s'
    params_chunks = (user_id,)
    all_chunks = db_mng.fetch_query(sql_chunks, params_chunks)
    sql_links = 'SELECT chunk_id, sentence_id FROM tbl_chunk_sentence_links WHERE user_id=%s'
    params_links = (user_id,)
    all_links = db_mng.fetch_query(sql_links, params_links)
    chunk_dict = {chunk['id']: {"label": chunk['learning_chunk'], "size": chunk['pronounced_count']} for chunk in all_chunks}
    net = Network()
    max_size = max(chunk["size"] for chunk in chunk_dict.values()) if chunk_dict else 1
    for chunk_id, chunk_data in chunk_dict.items():
        normalized_size = (chunk_data["size"] / max_size) * 20 + 5
        net.add_node(chunk_id, label=chunk_data["label"], size=normalized_size)
    edge_counts = {}
    for link in all_links:
        chunk_id = link['chunk_id']
        sentence_id = link['sentence_id']
        sql_related_chunks = 'SELECT chunk_id FROM tbl_chunk_sentence_links WHERE sentence_id=%s AND chunk_id!=%s'
        params_related_chunks = (sentence_id, chunk_id)
        related_chunks = db_mng.fetch_query(sql_related_chunks, params_related_chunks)
        for related_chunk in related_chunks:
            related_chunk_id = related_chunk['chunk_id']
            if chunk_id in chunk_dict and related_chunk_id in chunk_dict:
                if (chunk_id, related_chunk_id) not in edge_counts:
                    edge_counts[(chunk_id, related_chunk_id)] = 0
                edge_counts[(chunk_id, related_chunk_id)] += 1
    for (chunk_id, related_chunk_id), count in edge_counts.items():
        net.add_edge(chunk_id, related_chunk_id, width=count)
    net.options.interaction.zoomSpeed = 0.5
    net.options.physics.barnesHut.gravitationalConstant = -2000
    net.options.physics.barnesHut.centralGravity = 0.3
    net.options.physics.barnesHut.springLength = 100
    net.options.physics.barnesHut.springConstant = 0.4
    net.save_graph("dist/pyvis.html")
    with open('dist/pyvis.html', 'r') as file:
        html_content = file.read()
    return html_content

@api.route("/statistics", methods=["GET"])
@login_required
def get_statistics():
    user_id = session['user_id']
    try:
        today = datetime.today().date()
        dates = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(30)][::-1]

        
        chunk_registration_data = Statistics.get_chunk_registration_data(db_mng, user_id)
        chunk_registration_dict = {str(row['registration_date']): row['count'] for row in chunk_registration_data}
        
        
        chunk_sentence_registration_data = Statistics.get_chunk_sentence_registration_data(db_mng, user_id)
        chunk_sentence_registration_dict = {str(row['registration_date']): row['count'] for row in chunk_sentence_registration_data}
        
        
        chunk_pronounced_data = Statistics.get_chunk_pronounced_counts(db_mng, user_id)
        chunk_pronounced_dict = {str(row['date']): row['total_pronounced_count'] for row in chunk_pronounced_data}
        
        
        chunk_sentence_pronounced_data = Statistics.get_chunk_sentence_pronounced_counts(db_mng, user_id)
        chunk_sentence_pronounced_dict = {str(row['date']): row['total_pronounced_count'] for row in chunk_sentence_pronounced_data}

        chunk_registration_list = [chunk_registration_dict.get(date, 0) for date in dates]
        chunk_sentence_registration_list = [chunk_sentence_registration_dict.get(date, 0) for date in dates]
        chunk_pronounced_list = [chunk_pronounced_dict.get(date, 0) for date in dates]
        chunk_sentence_pronounced_list = [chunk_sentence_pronounced_dict.get(date, 0) for date in dates]

        result = {
            "dates": dates,
            "chunkRegistration": chunk_registration_list,
            "chunkSentenceRegistration": chunk_sentence_registration_list,
            "chunkPronounced": chunk_pronounced_list,
            "chunkSentencePronounced": chunk_sentence_pronounced_list,
        }
        return jsonify(result)
    except mysql.connector.Error as err:
        return jsonify({"error": "Error fetching data"}), 500
