import { KeyRound, CreditCard, ShieldCheck, FolderUp, UserPlus, Smartphone } from 'lucide-react';

const suggestions = [
    { icon: KeyRound, text: 'How do I reset my password?' },
    { icon: CreditCard, text: 'What are the pricing plans?' },
    { icon: ShieldCheck, text: 'How is my data secured?' },
    { icon: FolderUp, text: 'What are the file upload limits?' },
    { icon: UserPlus, text: 'How do I add team members?' },
    { icon: Smartphone, text: 'Is there a mobile app available?' },
];

const SuggestionChips = ({ onSelect }) => {
    return (
        <div className="suggestion-grid">
            {suggestions.map((item, index) => {
                const IconComponent = item.icon;
                return (
                    <button
                        key={index}
                        className="suggestion-chip"
                        onClick={() => onSelect(item.text)}
                    >
                        <span className="suggestion-chip-icon">
                            <IconComponent size={20} strokeWidth={1.8} />
                        </span>
                        {item.text}
                    </button>
                );
            })}
        </div>
    );
};

export default SuggestionChips;
