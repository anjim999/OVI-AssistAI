const StatusIndicator = ({ stages }) => {
    return (
        <div className="status-stages">
            {stages.map((stage, index) => (
                <div className="status-stage" key={index}>
                    <div className="status-dot" />
                    <span>{stage.message}</span>
                </div>
            ))}
        </div>
    );
};

export default StatusIndicator;

