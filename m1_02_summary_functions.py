"""
Summary and Validation Functions for Lab M1-02.
This module handles data integrity checks and analytics summaries.
"""

# --- TASK 2: VALIDATION HELPERS ---

def find_invalid_tickets(data_list):
    """Identifies tickets with missing or non-numeric resolution_minutes."""
    invalid_indices = []
    
    for index, record in enumerate(data_list):
        res = record.get("resolution_minutes")
        # Checking if it's not a number or if it's less than zero
        if not isinstance(res, (int, float)) or res < 0:
            invalid_indices.append(index)
            
    return invalid_indices

def check_missing_keys(data_list, required_keys):
    """Checks if any record is missing a mandatory key."""
    records_with_missing_keys = []
    
    for record in data_list:
        for key in required_keys:
            if key not in record:
                records_with_missing_keys.append(record["ticket_id"])
                break
                
    return records_with_missing_keys

# --- TASK 4: SUMMARY FUNCTIONS ---

def get_average_res_time(data):
    """Returns a dictionary: {category: average_time}"""
    stats = {} # Format: {category: [sum_of_minutes, count]}
    
    for record in data:
        cat = record['category']
        mins = record['resolution_minutes']
        
        if cat not in stats:
            stats[cat] = [0, 0]
        
        stats[cat][0] += mins
        stats[cat][1] += 1
    
    # Calculating final averages
    averages = {cat: (val[0] / val[1]) for cat, val in stats.items()}
    return averages

def get_ticket_counts_by_customer(data):
    """Returns a dictionary: {customer_id: count}"""
    counts = {}
    for record in data:
        cid = record['customer_id']
        counts[cid] = counts.get(cid, 0) + 1
    return counts

def get_escalation_metrics(data):
    """Returns a dictionary with overall rate and by-category rates."""
    total_tickets = len(data)
    total_escalated = sum(1 for r in data if r['escalated'])
    
    # Category breakdown
    cat_metrics = {}
    for record in data:
        cat = record['category']
        if cat not in cat_metrics:
            cat_metrics[cat] = {"total": 0, "esc": 0}
        
        cat_metrics[cat]["total"] += 1
        if record['escalated']:
            cat_metrics[cat]["esc"] += 1
            
    # Calculating rates
    report = {
        "overall_rate": total_escalated / total_tickets,
        "by_category": {cat: (m["esc"] / m["total"]) for cat, m in cat_metrics.items()}
    }
    return report