export function getPolitenessColor(politeness) {
    politeness = parseFloat(politeness);
    if (politeness >= 0 && politeness < 1) return '#3F51B5'; 
    if (politeness >= 1 && politeness < 2) return '#03A9F4'; 
    if (politeness >= 2 && politeness < 3) return '#4CAF50'; 
    if (politeness >= 3 && politeness < 4) return '#FF9800'; 
    if (politeness >= 4) return '#F44336'; 
    return 'grey';
  }
  