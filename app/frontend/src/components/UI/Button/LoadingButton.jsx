import React from "react";
import ButtonSpinner from "../../Spinner/ButtonSpinner";

const LoadingButton = ({children, isLoading, showChildrenOnLoad = true, ...props}) => {
    return (
        <button disabled={isLoading && true} {...props}>
            {isLoading
                ?
                <React.Fragment>
                    <ButtonSpinner/>
                    {showChildrenOnLoad && children}
                </React.Fragment>
                :
                <React.Fragment>
                    {children}
                </React.Fragment>
            }
        </button>
    );
};

export default LoadingButton;