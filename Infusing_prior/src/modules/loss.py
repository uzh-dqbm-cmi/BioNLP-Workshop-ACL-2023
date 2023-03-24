import torch
import torch.nn as nn


class LanguageModelCriterion(nn.Module):
    def __init__(self):
        super(LanguageModelCriterion, self).__init__()

    def forward(self, input, target, mask):
        # truncate to the same size
        if isinstance(input, type(torch.tensor(1))): # M2tr
            target = target[:, :input.size(1)]
            mask = mask[:, :input.size(1)]             
            output = -input.gather(2, target.long().unsqueeze(2)).squeeze(2) * mask
        else: # R2gen
            target = target[:, :input[0].size(1)]
            mask = mask[:, :input[0].size(1)]
            output = -input[0].gather(2, target.long().unsqueeze(2)).squeeze(2) * mask
        output = torch.sum(output) / torch.sum(mask)
        return output


def compute_loss(output, reports_ids, reports_masks):
    criterion = LanguageModelCriterion()
    loss = criterion(output, reports_ids[:, 1:], reports_masks[:, 1:]).mean()
    return loss

